from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from apps.common.config import DevelopMent

db_addr = DevelopMent.OPENFALCON_DB_ADDR
db_port = DevelopMent.OPENFALCON_DB_PORT
db_name = DevelopMent.OPENFALCON_DB_NAME
db_user = DevelopMent.OPENFALCON_DB_USER
db_pass = DevelopMent.OPENFALCON_DB_PASSWORD

engine = create_engine('mysql+pymysql://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}'.format(
    DBUSER=db_user,
    DBPASS=db_pass,
    DBHOST=db_addr,
    DBPORT=db_port
))

metadata = MetaData()
metadata.reflect(bind=engine, schema=db_name)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class endpoint_counter(Base):
    __table__ = metadata.tables['{}.endpoint_counter'.format(db_name)]


class endpoint(Base):
    __table__ = metadata.tables['{}.endpoint'.format(db_name)]


class tag_endpoint(Base):
    __table__ = metadata.tables['{}.tag_endpoint'.format(db_name)]


