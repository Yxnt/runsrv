from . import Base
from sqlalchemy import Column, INTEGER, NVARCHAR


class GitRepo(Base):
    __tablename__ = 'runsrv_git_repo'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    repo_id = Column(INTEGER, nullable=False, unique=True)
    repo_name = Column(NVARCHAR(100), nullable=False,unique=True)
    repo_url = Column(NVARCHAR(100), nullable=False)
    repo_desc = Column(NVARCHAR(100), nullable=True)
    repo_pub_path = Column(NVARCHAR(100))