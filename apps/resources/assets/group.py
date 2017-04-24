from flask_restful import Resource, reqparse, fields, marshal
from apps.tasks import group_save
from apps.tasks.db import host_to_group
from apps import db
from flask import current_app, jsonify
from apps.models import table

from collections import OrderedDict

res_fields = {
    "groupname": fields.String,
    "groupdesc": fields.String(attribute="description"),
    "clientnumber": fields.Integer(attribute="client_numbers"),
}


class Group(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('name', type=str, location='args')
    parse.add_argument('description', type=str, location='args')
    parse.add_argument('client', action='append', location='args')
    parse.add_argument("limit", type=int, location='args')
    parse.add_argument('offset', type=int, location='args')
    parse.add_argument('order', type=str, location='args')

    def get(self, groupname=None):
        args = self.parse.parse_args()
        data = []
        host = table['host']
        group = table['group']
        host_to_group = table['host_group']
        if args['offset']:
            page = args['offset'] / 10 +1
        else:
            page = 1

        if args['limit']:
            limit = args['limit']
        else:
            limit = 10

        group_all = group.query.all()
        group_data = group.query.order_by(group.group_name.asc()).paginate(page, limit, error_out=True)
        groups = group_data.items

        for i in groups:
            info = OrderedDict()
            group_id = i.group_id
            group_name = i.group_name
            group_desc = i.group_descript
            client_number = i.group_host_counter
            host_to_group_data = host_to_group.query.filter_by(group_id=group_id).all()
            info['groupname'] = group_name
            info['description'] = group_desc
            info['client_numbers'] = client_number
            # info['clients'] = []
            for l in host_to_group_data:
                host_id = l.host_id
                host_data = host.query.filter_by(host_id=host_id).first()
                host_name = host_data.host_name
                # info['clients'].append(host_name)

            data.append(marshal(info, res_fields))

        total = len(group_all)
        rows = data
        db.session.commit()

        return jsonify({"total": total, "rows": rows})

    def post(self):
        args = self.parse.parse_args()
        groupname = args['name']
        groupdesc = args['description']
        client = args['client']

        group_save.delay(groupname, groupdesc, len(client))
        host_to_group.apply_async((client, groupname), countdown=1)
