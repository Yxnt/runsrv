from flask_restful import Resource, reqparse, fields, marshal
from apps.tasks import group_save
from apps.tasks.db import host_to_group
from flask import jsonify, make_response
from apps.models import table, session
from apps.common.apiauth.auth import user_auth

from collections import OrderedDict

res_fields = {
    "groupname": fields.String,
    "groupdesc": fields.String(attribute="description"),
    "clientnumber": fields.Integer(attribute="client_numbers"),
    "id": fields.Integer(attribute="id")
}


class Group(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('name', type=str, location=['args', 'form'])
    parse.add_argument('description', type=str, location=['args', 'form'])
    parse.add_argument('client', action='append', location=['args', 'form'])
    parse.add_argument("limit", type=int, location='args')
    parse.add_argument('offset', type=int, location='args')
    parse.add_argument('order', type=str, location='args')

    decorators = [user_auth]

    def get(self, groupname=None):
        self.parse.add_argument('all', type=int, location='args')
        args = self.parse.parse_args()

        data = []
        host = table['host']
        group = table['group']
        host_to_group = table['host_group']

        if args.all == 1:
            return [i.group_name for i in session.query(group).all()]

        if args['offset']:
            page = args['offset']
        else:
            page = 0

        if args['limit']:
            limit = args['limit']
        else:
            limit = 10

        group_all = session.query(group).all()
        group_data = session.query(group).order_by(group.group_id.asc()).offset(page).limit(limit).all()
        groups = group_data

        for i in groups:
            info = OrderedDict()
            group_id = i.group_id
            group_name = i.group_name
            group_desc = i.group_descript
            client_number = i.group_host_counter
            host_to_group_data = session.query(host_to_group).filter_by(group_id=group_id).all()
            info['groupname'] = group_name
            info['description'] = group_desc
            info['client_numbers'] = client_number
            info['id'] = group_id

            for l in host_to_group_data:
                host_id = l.host_id
                host_data = session.query(host).filter_by(host_id=host_id).first()
                host_name = host_data.host_name

            data.append(marshal(info, res_fields))

        total = len(group_all)
        rows = data
        session.commit()

        return jsonify({"total": total, "rows": rows})

    def post(self):
        self.parse.add_argument('delete', type=int, location='form')
        self.parse.add_argument('groups', type=str, action='append', location='form')

        args = self.parse.parse_args()

        groupname = args['name']
        groupdesc = args['description']
        client = args['client']

        if args.delete == 1 and args.groups:
            for i in args.groups:
                group = session.query(table['group']).filter(table['group'].group_id == i).first()
                for i in group.host:
                    session.delete(i)
                    session.delete(group)

            session.commit()
            return jsonify(message="删除成功")
        elif args.delete == 1:
            return make_response(jsonify(message="未选中组"), 400)

        group_save.delay(groupname, groupdesc, len(client))
        host_to_group.apply_async((client, groupname), countdown=1)
