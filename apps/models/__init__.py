from apps.common.config.config import DevelopMent

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(DevelopMent.SQLALCHEMY_DATABASE_URI,pool_size=10 , max_overflow=-1, pool_recycle=1200,echo=False)
metadata = MetaData()
metadata.reflect(bind=engine, schema='runsrv')
Session = sessionmaker(bind=engine,)
session = Session()
Base = declarative_base()


from apps.models.user import User
from apps.models.host import Host
from apps.models.group import Group, Host_Group
from apps.models.monitor import Monitor
from apps.models.git import GitRepo

table = {
    "user": User,
    "host": Host,
    "group": Group,
    "host_group": Host_Group,
    'gitrepo':GitRepo
}
