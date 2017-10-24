import os

from flask_restful import Resource, reqparse
from apps.models import GitRepo, session, Group, Host
from apps.tasks import saltstack
from apps.common.apiauth.auth import user_auth
from flask import current_app, send_from_directory, send_file
import werkzeug
import re
from time import sleep


class Statesls(Resource):
    parser = reqparse.RequestParser()

    def post(self):
        pass


class Git(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('reponame', type=str, location='form')
    parser.add_argument('minions', type=str, location='form', action='append')
    parser.add_argument('username', type=str, location='form')
    parser.add_argument('password', type=str, location='form')
    parser.add_argument('groups', type=str, location='form')
    parser.add_argument('module', type=str, location='form')
    parser.add_argument('tag', type=str, location='form')
    decorators = [user_auth]

    def post(self):
        args = self.parser.parse_args()
        repo = session.query(GitRepo).filter(GitRepo.repo_name == args.reponame).first()
        modules = {
            "clone": "git.clone",
            "fetch": "git.fetch",
            "checkout": "git.checkout",
            "pull": "git.pull"
        }
        module = modules[args.module]
        repo_url = repo.repo_url
        repo_path = repo.repo_pub_path

        if args.groups:
            client = [i.host.host_name for i in
                      session.query(Group).filter(Group.group_name == args.groups).first().host]
        else:
            client = args.minions

        if module == "git.clone":
            salt_args = [repo_path, repo_url, "opts='--depth 1'", 'https_user=%s' % args.username,
                         'https_pass=%s' % args.password]
        elif module == "git.pull":
            salt_args = [repo_path, "opts='origin master'"]
        elif module == "git.fetch":
            salt_args = [repo_path, "opts='--tags'"]

            fetch = saltstack.module.delay(module=module, target=client, args=salt_args)
            if fetch.get():
                module = 'git.checkout'
                salt_args = [repo_path, "rev='%s'" % args.tag]

        else:
            salt_args = [repo_path, "rev='%s'" % args.tag]

        result = saltstack.module.delay(module=module, target=client, args=salt_args)

        return result.get(timeout=5)


class LookJid(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('jid', type=int, location='args')
    decorators = [user_auth]

    def get(self):
        args = self.parser.parse_args()

        return current_app.salt.jid(args.jid)


class Cmd(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('minions', type=str, location='form', action='append')
    parser.add_argument('groups', type=str, location='form')
    parser.add_argument('cmd', type=str, location='form')

    decorators = [user_auth]

    def post(self):
        args = self.parser.parse_args()
        if args.groups:
            client = [i.host.host_name for i in
                      session.query(Group).filter(Group.group_name == args.groups).first().host]
        else:
            client = args.minions

        module = 'cmd.run'

        salt_args = [args.cmd]

        result = saltstack.module.delay(module=module, target=client, args=salt_args)

        return result.get(timeout=2)


class File(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('opt', type=str, location='form')
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
    parser.add_argument('minions', type=str, location='form', action='append')
    parser.add_argument('groups', type=str, location='form')

    decorators = [user_auth]

    def post(self):
        args = self.parser.parse_args()

        if args.groups:
            client = [i.host.host_name for i in
                      session.query(Group).filter(Group.group_name == args.groups).first().host]
        else:
            client = args.minions

        file = args['file']

        module = 'cp.get_file'

        file.save('/srv/salt/tmp/file/%s' % file.filename)

        salt_args = ["dest=%s" % args.opt, "path=%s" % "salt://tmp/file/%s" % file.filename]

        result = saltstack.module.delay(module=module, target=client, args=salt_args)

        return result.get(timeout=10)


class FileDownload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('minion', type=str, location=['json', 'form', 'args'])
    parser.add_argument('id', type=int, location=['json', 'form'])
    parser.add_argument('name', type=str, location=['json', 'form', 'args'])

    decorators = [user_auth]

    def get(self):
        args = self.parser.parse_args()
        client = args.minion
        path = args.name

        modules = 'cp.push'

        hostos = session.query(Host).filter(Host.host_name == client).first().host_os
        session.commit()

        if re.match(r".*Linux.*", hostos):
            salt_args = ['path=/%s' % path, 'keep_symlinks=True']
        else:
            salt_args = ['path=%s' % path, 'keep_symlinks=True']
            path="/".join(path.split('/')[1:])

        result = saltstack.module.delay(module=modules, target=client, args=salt_args)
        jid = result.get(timeout=2)['return'][0]['jid']

        while True:
            ret = current_app.salt.jid(jid)
            
            if ret['return'][0]:
                break
            sleep(1)

        file = "{root}/{minion}/files/{path}".format(
            root=current_app.config['MINIONS_FILE_ROOT'],
            minion=client,
            path=path
        )

        return send_file(file, as_attachment=True)

    def post(self):
        args = self.parser.parse_args()
        client = args.minion
        path = args.name
        pid = args.id

        if path:
            modules = "file.getfile"
            salt_args = ["dire=%s" % path, "id='%d'" % pid]
        else:
            salt_args = []
            hostos = session.query(Host).filter(Host.host_name == client).first().host_os

            if re.match(r".*Linux.*", hostos):
                modules = "file.getfile"
                salt_args = ["dire=/", "id='0'"]
            else:
                modules = "file.getdisk"

        result = saltstack.module.delay(module=modules, target=client, args=salt_args)
        jid = result.get(timeout=10)['return'][0]['jid']
        session.commit()

        while True:
            ret = current_app.salt.jid(jid)
            if ret:
                for k, v in current_app.salt.jid(jid)['return'][0].items():
                    return v
            sleep(1)