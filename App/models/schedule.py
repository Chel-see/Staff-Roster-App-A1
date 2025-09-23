from App.database import db


class Schedule(db.Model):
    __tablename__='schedule'
    id=db.Column(db.Integer,primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    available_id = db.Column(db.Integer, db.ForeignKey('available.id'), nullable=False)

    staff=db.relationship("Staff", back_populates="schedule")
    available = db.relationship("Available", back_populates="schedule")

   
   
    def __init__(self,staff_id,available_id) :
        self.staff_id=staff_id
        self.available_id=available_id
     



    

