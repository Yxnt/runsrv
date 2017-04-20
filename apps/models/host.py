from apps import db

runsrv_host_groups = db.Table(
    'runsrv_host_groups',
    db.Column('id',db.INTEGER,primary_key=True),
    db.Column("host_id", db.INTEGER, db.ForeignKey("runsrv_host.host_id")),
    db.Column("group_id", db.INTEGER, db.ForeignKey("runsrv_group.group_id")),
)


class Host(db.Model):
    __tablename__ = 'runsrv_host'
    host_id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    host_name = db.Column(db.NVARCHAR(100), unique=True, nullable=False)
    host_ip = db.Column(db.NVARCHAR(15), unique=True, nullable=False)
    host_location = db.Column(db.NVARCHAR(50), default="香港")
    host_os = db.Column(db.NVARCHAR(50), nullable=False)
    host_stats = db.Column(db.NVARCHAR(4), nullable=False)
    host_groups = db.relationship('Group', secondary=runsrv_host_groups, backref=db.backref('runsrv_host'), lazy='dynamic')

    def __init__(self, hostname, ip, os, stats, location=None):
        self.host_name = hostname
        self.host_ip = ip
        self.host_location = location
        self.host_os = os
        self.host_stats = stats
