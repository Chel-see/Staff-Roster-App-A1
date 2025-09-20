from App.database import db


class Schedule(db.Model):
    __tablename__='schedule'
    id=db.Column(db.Integer,primary_key=True)
    staff_id=db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=False)
    date_assigned=db.Column(db.DateTime)
    timeslot=db.Column(db.DateTime)


    

