from apps import db


class Host(db.Model):
    __tablename__ = 'runsrv_host'
    host_id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    host_name = db.Column(db.NVARCHAR(100), unique=True, nullable=False)
    host_ip = db.Column(db.NVARCHAR(15), unique=True, nullable=False)
    host_location = db.Column(db.NVARCHAR(12))
    host_os = db.Column(db.NVARCHAR(30), nullable=False)
    host_stats = db.Column(db.NVARCHAR(4), nullable=False)

    def __init__(self, hostname, ip, os, stats, location=None):
        self.host_name = hostname
        self.host_ip = ip
        self.host_location = location
        self.host_os = os
        self.host_stats = stats
