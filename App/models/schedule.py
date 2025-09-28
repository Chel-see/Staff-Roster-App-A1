from App.database import db


class Schedule(db.Model):
    __tablename__='schedule'
    id=db.Column(db.Integer,primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    available_id = db.Column(db.Integer, db.ForeignKey('available.id'), nullable=False)

    #staff=db.relationship("Staff", back_populates="schedule")
    #available = db.relationship("Available", back_populates="schedule")
    shift = db.relationship("Shift", backref="schedule", uselist=False, cascade="all, delete-orphan")

    def __init__(self,staff_id,available_id):
        self.staff_id=staff_id
        self.available_id=available_id
     
    def __repr__(self):
        return f"|{self.id}-{self.staff.name} {self.available.day} {self.available.start_time}-{self.available.end_time}|"



    

