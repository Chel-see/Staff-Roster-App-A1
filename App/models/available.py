from App.database import db

class Available(db.Model):
    __tablename__='available'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10))  
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))
    status= db.Column(db.String(20))

    schedule = db.relationship(
        "Schedule",
        backref="available",
        cascade="all, delete-orphan"   
    )
  

    def __init__(self,day,start_time,end_time):
        self.day=day
        self.start_time=start_time
        self.end_time=end_time
        self.status="available"

    def set_status(self,status):
        self.status=status

    def __repr__(self):
        return f"|{self.id}-{self.day} {self.start_time}-{self.end_time} {self.status}|"

        

  
