from apps import celery
from requests import session
from apps.common.config import DevelopMent
from urllib import parse as urlparse
from apps.models import GitRepo
from apps.models import session as db
import re


@celery.task
def get_all_projects():

    allproject_url = urlparse.urljoin(DevelopMent.GITLAB_ADDR, 'api/v3/projects/all')
    response = get_repo_info(allproject_url, DevelopMent.GITLAB_TOKEN_HEADER)
    header = response.headers['Link']

    repo_update(response.json())

    link = re.compile(r'([^<|>|;|,|\s]+)')
    links = link.findall(header)
    rel = re.compile('rel="(\w+)"')
    n = -1

    for i in range(len(links) // 2):
        n += 2

        if (rel.search(links[n]).group(1)) == 'last':
            last_num = re.match('.*(\?page=(\d))', links[i * 2]).group(2)

            break

    for i in range(1, int(last_num)):
        i += 1
        url = "%s?page=%d" % (allproject_url, i)
        response = get_repo_info(url, DevelopMent.GITLAB_TOKEN_HEADER)
        repo_update(response.json())


def get_repo_info(url, header):
    sessions = session()
    response = sessions.get(url, headers=header)
    return response


def repo_update(data):
    for i in data:
        description = i['description']
        name = i['name']
        id = i['id']
        url = "%s" % (urlparse.urljoin(DevelopMent.GITLAB_ADDR, "%s.git" % i['path_with_namespace']))

        if db.query(GitRepo).filter(GitRepo.repo_id==id, GitRepo.repo_name==name).first():
            continue
        else:
            db.merge(GitRepo(repo_id=id, repo_name=name, repo_url=url, repo_desc=description))
    db.commit()
