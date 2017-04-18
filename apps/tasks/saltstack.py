from apps import celery
from flask import current_app
from apps.models import Host
from apps import db
from collections import OrderedDict


@celery.task
def update_host_list_to_db():
    # 获取主机基本信息，并存储
    host = Host
    ret = OrderedDict()
    client_number = 0
    ret['clients'] = []
    for k, v in current_app.salt.minions()['return'][0].items():
        data = {}
        hostname = k
        if 'oscodename' in v:
            os = v['oscodename']
        else:
            os = v['osfullname']
        network_dev = v['ip_interfaces']
        for k, v in network_dev.items():
            if "127.0.0.1" in v or "::1" in v:
                continue
            hostip = v[0]

        status = "UP"
        data['hostname'] = hostname
        data['ip'] = hostip
        data['location'] = "香港"
        data['osinfo'] = os
        data['group'] = ""
        data['status'] = "UP"
        client_number +=1
        query = host.query.filter_by(host_ip=hostip).first()
        if not query:
            hostinfo = host(hostname=hostname, ip=hostip, os=os, stats=status)
            db.session.add(hostinfo)
        ret['client_number'] = client_number
        ret['clients'].append(data)
    db.session.commit()

    return ret

