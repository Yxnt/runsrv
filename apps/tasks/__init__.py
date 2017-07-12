from apps.tasks.saltstack import get_minion_info, module
from apps.tasks.redis import system_operator, redis_save
from apps.tasks.db import group_save, host_to_group
from apps.tasks.monitor import hostmonitor
from apps.tasks.sender import send_email
from apps.tasks.gitlab import get_all_projects
