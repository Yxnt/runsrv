from apps import celery
from apps.models import table,session


@celery.task
def group_save(groupname, desc, counter):
    """保存组信息"""
    group = table['group']
    data = group(group_name=groupname, group_host_counter=counter, group_descript=desc)
    session.add(data)
    session.commit()


@celery.task
def host_to_group(clients, groupname):
    """保存主机组关系"""
    hosttogroup = table['host_group']
    host = table['host']
    group = table['group']

    for client in clients:
        host_id = session.query(host.host_id).filter_by(host_name=client).first()

        group_id = session.query(group.group_id).filter_by(group_name=groupname).first()

        if host_id and group_id:
            relationship = hosttogroup(host_id=host_id.host_id,group_id=group_id.group_id)
            session.add(relationship)

    session.commit()

