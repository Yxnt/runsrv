from apps.models.user import User
from apps.models.host import Host
from apps.models.group import Group,Host_Group

table = {
    "user":User,
    "host":Host,
    "group":Group,
    "host_group":Host_Group
}