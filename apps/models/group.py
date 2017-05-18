from . import Base,metadata
from sqlalchemy import INTEGER,Column,NVARCHAR

class Group(Base):
    __tablename__ = 'runsrv_group'
    group_id = Column(INTEGER, primary_key=True, autoincrement=True)
    group_name = Column(NVARCHAR(20), unique=True)
    group_host_counter = Column(INTEGER)
    group_descript = Column(NVARCHAR(200))


class Host_Group(Base):
    __table__ = Base.metadata.tables['runsrv_host_groups']
