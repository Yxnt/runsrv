from datetime import datetime
from apps import login
from apps.models import Base
from sqlalchemy import Column, INTEGER, DATETIME, NVARCHAR
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from apps.models import session


class User(UserMixin, Base):
    """
    用户表，存放了所有的用户
    """
    __tablename__ = 'runsrv_user'
    user_id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(NVARCHAR(80), unique=True, nullable=False)
    password = Column(NVARCHAR(93), unique=True, nullable=True)
    email = Column(NVARCHAR(50), unique=True, nullable=True)
    regtime = Column(DATETIME, nullable=False)
    status = Column(NVARCHAR(10), nullable=False)

    def __init__(self, username, password=None, email=None, status=None):
        self.username = username
        if password == None:
            password = '123'
        self.hash_password(password)
        self.email = email
        self.regtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if status == None:
            self.status = "disabled"
        self.status = status

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id

    def is_active(self):
        pass


@login.user_loader
def load_user(user_id):
    id = session.query(User).get(user_id)
    session.commit()
    return id
