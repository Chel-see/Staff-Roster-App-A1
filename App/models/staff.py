from App.database import db
from App.models import User

class Staff(User): # inherit from Parent class User
    __tablename__='staff'
    id=db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)

    __mapper_args__={'polymorphic_identity':'staff'}


    def __repr__(self):
        return f"{self.username}"