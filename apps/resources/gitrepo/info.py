from flask_restful import Resource, reqparse
from apps.models import GitRepo, session
from flask import jsonify,make_response
from apps.tasks import get_all_projects
from apps.common.apiauth.auth import user_auth
from requests import get as req_get
from urllib import parse as urlparse
from apps.common.config import DevelopMent


class GitInfo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('order', type=str, location='args')
    parser.add_argument('offset', type=int, location='args')
    parser.add_argument('limit', type=int, location='args')

    decorators = [user_auth]

    def get(self):
        self.parser.add_argument('all', type=int, location='args')
        args = self.parser.parse_args()
        offset = args.offset
        order = args.order
        limit = args.limit

        if order == None:
            order = 'asc'

        order_table = {
            'asc': GitRepo.repo_id.asc(),
            'desc': GitRepo.repo_id.desc()
        }

        if args.all == 1:
            return [i.repo_name for i in session.query(GitRepo).all()]

        total = len(session.query(GitRepo).all())

        data = session.query(GitRepo).order_by(order_table[order]).offset(offset).limit(limit).all()
        rows = []

        for i in data:
            rows.append({"reponame": i.repo_name,
                         "repodesc": i.repo_desc,
                         "repoaddr": i.repo_url,
                         "repopubpath": i.repo_pub_path, "repoid": i.repo_id})

        return jsonify({"total": total, "rows": rows})

    def post(self):
        self.parser.add_argument('repoid', type=int, location="form")
        self.parser.add_argument('repopubpath', type=str, location="form")
        self.parser.add_argument('updategit', type=int, location='form')

        args = self.parser.parse_args()
        id = args.repoid
        path = args.repopubpath
        update = args.updategit

        if update == 1:
            get_all_projects.delay()
            return "后台更新中"

        session.query(GitRepo).filter(GitRepo.repo_id == id).update({GitRepo.repo_pub_path: path})
        session.commit()

        return jsonify(message="更新成功")


class GitTag(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('reponame', type=str, location=['form','args'])

    decorators = [user_auth]

    def get(self):
        args = self.parser.parse_args()
        repo = args.reponame
        if repo:
            repo_id = session.query(GitRepo).filter(GitRepo.repo_name == repo).first().repo_id
            tag_url = urlparse.urljoin(DevelopMent.GITLAB_ADDR, '/api/v3/projects/{id}/repository/tags'.format(id=repo_id))
            response = req_get(tag_url,headers=DevelopMent.GITLAB_TOKEN_HEADER).json()
            return [i["name"] for i in response]
        return make_response(jsonify({"message":"缺少项目名称"}),400)
