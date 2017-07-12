from apps import celery
from flask import current_app
from apps.models import Host, session
from collections import OrderedDict
from ipaddress import IPv4Address as ipv4


@celery.task
def get_minion_info():
    minions = current_app.salt.minions()['return'][0]

    # for k, v in minions.items():
    #     data = {}
    #     hostname = v['fqdn']
    #     if 'oscodename' in v:
    #         os = v['oscodename']
    #     else:
    #         os = v['osfullname']
    #
    #     ip_all = v['ipv4']
    #     for i in ip_all:
    #         if ipv4(i).is_private:
    #             hostip = i
    #             break
    #
    #     data['minion_id'] = k
    #     data['hostname'] = hostname
    #     data['ip'] = hostip
    #
    #     data['osinfo'] = os
    #     data['group'] = ""
    #
    #     client_number += 1
    #     query = session.query(host).filter_by(host_minion_id=k).first()
    #     if not query:
    #         hostinfo = host(hostname=hostname, ip=hostip, os=os, host_minion_id=k)
    #         session.add(hostinfo)
    #     ret['client_number'] = client_number
    #     ret['clients'].append(data)
    #     session.commit()

    return minions


@celery.task
def statesls():
    pass


@celery.task
def module(module, args, target):
    data = [{'client': 'local_async', 'tgt': target, 'fun': module, 'arg': args, 'expr_form': 'list'}]
    return current_app.salt.run(data)
