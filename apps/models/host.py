from . import Base
from sqlalchemy import Table,INTEGER,ForeignKey,Column,NVARCHAR
from sqlalchemy.orm import relationship, backref

runsrv_host_groups = Table(
    'runsrv_host_groups',Base.metadata,
    Column('id',INTEGER,primary_key=True),
    Column("host_id", INTEGER, ForeignKey("runsrv_host.host_id")),
    Column("group_id", INTEGER, ForeignKey("runsrv_group.group_id")),
)


class Host(Base):
    __tablename__ = 'runsrv_host'
    host_id = Column(INTEGER, primary_key=True, autoincrement=True)
    host_minion_id = Column(NVARCHAR(100), unique=True, nullable=False)
    host_name = Column(NVARCHAR(100), unique=True, nullable=False)
    host_ip = Column(NVARCHAR(15), unique=True, nullable=False)
    host_os = Column(NVARCHAR(50), nullable=False)
    host_groups = relationship('Group', secondary=runsrv_host_groups, backref=backref('runsrv_host'), lazy='dynamic')

    def __init__(self, hostname, ip, os, stats, location=None):
        self.host_name = hostname
        self.host_ip = ip
        self.host_location = location
        self.host_os = os
        self.host_stats = stats

