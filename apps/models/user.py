from datetime import datetime
from apps import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    用户表，存放了所有的用户
    """
    __tablename__ = 'runsrv_user'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.NVARCHAR(80), unique=True, nullable=False)
    password = db.Column(db.NVARCHAR(93), unique=True, nullable=True)
    email = db.Column(db.NVARCHAR(50), unique=True, nullable=True)
    regtime = db.Column(db.DATETIME, nullable=False)
    status = db.Column(db.NVARCHAR(10), nullable=False)

    def __init__(self, username, password=None, email=None):
        self.username = username
        if password == None:
            password = '123'
        self.hash_password(password)
        self.email = email
        self.regtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = "disabled"

    def hash_password(self,password):
        self.password = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password,password)

