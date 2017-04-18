from flask_restful import Resource, reqparse
from apps.tasks import group_save
from apps.tasks.db import host_to_group
from flask import current_app
from apps.models import table

class Group(Resource):
    parse = reqparse.RequestParser()
    groupname = parse.add_argument('name', type=str, help="参数错误")
    groupdesc = parse.add_argument('description', type=str, help="参数错误")
    clients = parse.add_argument('client', action='append')

    def get(self, groupname=None):
        args = self.parse.parse_args()
        data = []
        host = table['host']
        group = table['group']
        host_to_group = table['host_group']

        group_data = group.query.all()

        for i in group_data:
            info = {}
            group_id =i.group_id
            group_name = i.group_name
            group_desc = i.group_descript
            client_number = i.group_host_counter
            host_to_group_data = host_to_group.query.filter_by(group_id=group_id).all()
            info['groupname'] = group_name
            info['description'] = group_desc
            info['client_numbers'] = client_number
            info['clients'] = []
            for l in  host_to_group_data:
                host_id = l.host_id
                host_data = host.query.filter_by(host_id=host_id).first()
                host_name = host_data.host_name

                info['clients'].append(host_name)

            data.append(info)

        return current_app.make_res(200,200,"获取成功",groups=data)

    def post(self):
        args = self.parse.parse_args()
        groupname = args['name']
        groupdesc = args['description']
        client = args['client']

        group_save.delay(groupname, groupdesc, len(client))
        host_to_group.delay(client, groupname)
