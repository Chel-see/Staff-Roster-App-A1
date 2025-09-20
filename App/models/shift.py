from App.database import db


class Shift(db.Model):
    __tablename__='shift'
    id=db.Column(db.Integer,primary_key=True)
    staff_id=db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=False)
    schedule_id=db.Column(db.Integer,db.ForeignKey('schedule.id'),nullable=False)
    timeIn=db.Column(db.DateTime)
    timeOut=db.Column(db.DateTime)