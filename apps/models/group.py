from apps import db


class Group(db.Model):
    __tablename__ = 'runsrv_group'
    group_id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    group_name = db.Column(db.NVARCHAR(20), unique=True)
    group_host_counter = db.Column(db.INTEGER)
    group_descript = db.Column(db.NVARCHAR(200))


class Host_Group(db.Model):
    __table__ = db.Model.metadata.tables['runsrv_host_groups']
