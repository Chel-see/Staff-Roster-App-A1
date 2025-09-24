from App.database import db


class Shift(db.Model):
    __tablename__='shift'
    id=db.Column(db.Integer,primary_key=True)
    staff_id=db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=False)
    schedule_id=db.Column(db.Integer,db.ForeignKey('schedule.id'),nullable=False)
    timeIn=db.Column(db.String(10), nullable=True)
    timeOut=db.Column(db.String(10), nullable=True)
    schedule=db.relationship("Schedule",backref="shift")

    def __init__(self,staff_id,schedule_id,timeIn,timeOut):
        self.staff_id=staff_id
        self.schedule_id=schedule_id
        self.timeIn=timeIn
        self.timeOut=timeOut

    def set_timeIn(self,timeIn):
        self.timeIn=timeIn

    def set_timeOut(self,timeOut):
        self.timeOut=timeOut
        
    def __repr__(self):
        return f"<Shift {self.id} - Staff ID: {self.staff_id} - Schedule ID: {self.schedule_id} - Time In: {self.timeIn} - Time Out: {self.timeOut}>"
