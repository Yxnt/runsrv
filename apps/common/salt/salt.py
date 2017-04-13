import requests
import urllib.parse as urljoin

from json import dumps, loads
from flask import current_app


class SaltApi(object):
    schema = None
    token = None
    expirse = None
    token_name = current_app.config['LOGIN_TOKEN_NAME']

    def __init__(self, user, passwd, host, port, eauth, is_ssl):
        self.user = user
        self.passwd = passwd
        self.eauth = eauth
        assert isinstance(is_ssl, bool), "is_ssl should be Bool"

        if is_ssl:
            self.schema = 'https'
        else:
            self.schema = 'http'

        self.url = '{schmea}://{host}:{port}'.format(schmea=self.schema, host=host, port=port)

    def __header(self):
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        token = current_app.redis.get(self.token_name)

        if token:
            header.update(loads(token.decode('utf-8')))

        return header

    def req(self, uri):
        url = urljoin.urljoin(self.url, uri)
        content = requests.get(url, headers=self.__header())
        if content.status_code == 200:
            return content.json()

    def reqp(self, data, header=None, uri=None):
        if uri:
            url = "{url}/{uri}".format(url=self.url, uri=uri)
        else:
            url = self.url

        if header:
            headers = self.__header().update(header)
        else:
            headers = self.__header()

        content = requests.post(url, json=data, headers=headers)

        if content.status_code == 200:
            return content.json()

    def login(self):

        data = {
            "username": self.user,
            "password": self.passwd,
            "eauth": self.eauth
        }

        content = self.reqp(uri='login', data=data)
        if content:
            content = content['return'][0]
            self.token = content['token']
            self.expirse = int(content['expire'] - content['start'])
            current_app.redis.set(self.token_name, dumps({'X-Auth-Token': self.token}), self.expirse)
            return True

    def minions(self, minion=None):
        if minion != None:
            uri = '/minions/%s' % minion
            return self.req(uri)
        else:
            minion_list = []
            response = self.req('/minions')['return'][0]
            for k, v in response.items():
                minion_list.append(k)
            return current_app.save_redis(200, '获取成功', minions=minion_list)

    def keys(self):
        pass

    def jid(self):
        pass

    def stats(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    user = 'salt'
    passwd = '123'
    host = '10.19.80.12'
    port = 8000
    eauth = 'pam'
    is_ssl = False

    s = SaltApi(user=user,
                passwd=passwd,
                host=host,
                port=port,
                eauth=eauth,
                is_ssl=is_ssl)
    s.login()
    print(s.minions())