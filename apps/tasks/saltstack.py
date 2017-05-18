from apps import celery
from flask import current_app
from apps.models import Host,session
from collections import OrderedDict
from ipaddress import IPv4Address as ipv4


@celery.task
def update_host_list_to_db():
    # 获取主机基本信息，并存储
    host = Host
    ret = OrderedDict()
    client_number = 0
    ret['clients'] = []
    for k, v in current_app.salt.minions()['return'][0].items():
        data = {}
        hostname = v['fqdn']
        if 'oscodename' in v:
            os = v['oscodename']
        else:
            os = v['osfullname']
        ip_all = v['ipv4']
        for i in ip_all:
            if ipv4(i).is_private:
                hostip = i
                break

        status = "UP"
        data['hostname'] = hostname
        data['ip'] = hostip
        data['location'] = "香港"
        data['osinfo'] = os
        data['group'] = ""
        data['status'] = "UP"
        client_number += 1
        query = session.query(host).filter_by(host_ip=hostip).first()
        if not query:
            hostinfo = host(hostname=hostname, ip=hostip, os=os, stats=status)
            session.add(hostinfo)
        ret['client_number'] = client_number
        ret['clients'].append(data)
        session.commit()

    return ret
