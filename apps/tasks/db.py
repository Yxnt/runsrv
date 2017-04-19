from apps import celery, db
from apps.models import table


@celery.task
def group_save(groupname, desc, counter):
    """保存组信息"""
    group = table['group']
    data = group(group_name=groupname, group_host_counter=counter, group_descript=desc)
    db.session.add(data)
    db.session.commit()


@celery.task
def host_to_group(clients, groupname):
    """保存主机组关系"""
    hosttogroup = table['host_group']
    host = table['host']
    group = table['group']

    for client in clients:
        host = host.query.filter_by(host_name=client).first()
        group = group.query.filter_by(group_name=groupname).first()
        if host:
            relationship = hosttogroup(host_id=host.host_id,group_id=group.group_id)
            db.session.add(relationship)

    db.session.commit()

