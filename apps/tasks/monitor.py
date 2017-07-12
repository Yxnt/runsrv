from apps import celery
from apps.common.config import DevelopMent
from apps.models.openfalcon import session, endpoint
from requests import post
from json import dumps
from apps.models import Monitor, session as runsrv_session
import time


@celery.task
def hostmonitor():
    monitor_addr = "http://{}/api/falcon/query/graph/history".format(DevelopMent.MONITOR_ADDR)
    clients = session.query(endpoint).all()
    session.commit()
    end_time = int(time.time())
    start_time = end_time - 60
    data = {"start": start_time, "end": end_time, "cf": "AVERAGE", "endpoint_counters": []}
    for i in clients:
        data['endpoint_counters'].append({"endpoint": i.endpoint, "counter": "cpu.idle"})
        data['endpoint_counters'].append({"endpoint": i.endpoint, "counter": "mem.memfree.percent"})
        data['endpoint_counters'].append({"endpoint": i.endpoint, "counter": "agent.alive"})

    data['endpoint_counters'] = dumps(data['endpoint_counters'])

    response = post(monitor_addr,
                    data=dumps(data),
                    headers={"Content-Type": "application/json"})

    ret = response.json()

    LEVEL = {
        1: "INFO",
        2: "WARNING",
        3: "ERROR"
    }

    for i in ret:
        hostname = i['endpoint']
        if i['counter'] == "agent.alive":
            for l in i['Values']:
                value = l["value"]
                if value == None:
                    type = "host"
                    if not runsrv_session.query(Monitor).filter(Monitor.type == type, Monitor.hostname == hostname,
                                                                Monitor.level == LEVEL[3]).first():
                        monitor = Monitor(hostname, "主机已离线", LEVEL[3], 1, type)
                        runsrv_session.add(monitor)
                    break

        if i['counter'] == 'cpu.idle':
            for l in i['Values']:
                value = l["value"]
                if value == None:
                    type = "cpu"
                    if not runsrv_session.query(Monitor).filter(Monitor.type == type, Monitor.hostname == hostname,
                                                                Monitor.level == LEVEL[3]).first():
                        monitor = Monitor(hostname, "CPU数据异常", LEVEL[3], 1, type)
                        runsrv_session.add(monitor)
                    break
                elif value < 10:
                    type = "cpu"
                    if not runsrv_session.query(Monitor).filter(Monitor.type == type, Monitor.hostname == hostname,
                                                                Monitor.level == LEVEL[2]).first():
                        monitor = Monitor(hostname, "CPU可用率不足10%", LEVEL[2], 1, type)
                        runsrv_session.add(monitor)
                    break

        if i['counter'] == 'mem.memfree.percent':
            for l in i['Values']:
                value = l["value"]
                if value == None:
                    type = "memory"
                    if not runsrv_session.query(Monitor).filter(Monitor.type == type, Monitor.hostname == hostname,
                                                                Monitor.level == LEVEL[3]).first():
                        monitor = Monitor(hostname, "内存数据异常", LEVEL[3], 1, type)
                        runsrv_session.add(monitor)
                    break
                elif value < 10:
                    type = "memory"
                    if not runsrv_session.query(Monitor).filter(Monitor.type == type, Monitor.hostname == hostname,
                                                                Monitor.level == LEVEL[2]).first():
                        monitor = Monitor(hostname, "内存可用率不足10%", LEVEL[2], 1, type)
                        runsrv_session.add(monitor)
                    break

        runsrv_session.commit()
