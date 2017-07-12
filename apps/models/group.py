from . import Base
from sqlalchemy import INTEGER, Column, NVARCHAR
from sqlalchemy.orm import relationship, backref


class Group(Base):
    __tablename__ = 'runsrv_group'
    group_id = Column(INTEGER, primary_key=True, autoincrement=True)
    group_name = Column(NVARCHAR(20), unique=True)
    group_host_counter = Column(INTEGER)
    group_descript = Column(NVARCHAR(200))

    host = relationship('Host_Group', backref=backref('group'))


class Host_Group(Base):
    __table__ = Base.metadata.tables['runsrv_host_groups']

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    host = relationship('Host', backref=backref('runsrv_host_groups'))
