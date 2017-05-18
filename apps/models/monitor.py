from datetime import datetime

from . import Base
from sqlalchemy import Column,INTEGER,NVARCHAR,BOOLEAN,DATETIME


class Monitor(Base):
    __tablename__ = 'runsrv_monitor'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    hostname = Column(NVARCHAR(100), nullable=False)
    message = Column(NVARCHAR(1000), nullable=False)
    level = Column(NVARCHAR(10), nullable=False)
    operator = Column(BOOLEAN, nullable=False)
    type = Column(NVARCHAR(100), nullable=False)
    c_time = Column(DATETIME, nullable=False)

    def __init__(self, hostname, message, level, operator, type):
        self.hostname = hostname
        self.message = message
        self.level = level
        self.operator = operator
        self.type = type
        self.c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
