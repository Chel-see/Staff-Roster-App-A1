from App.database import db
from App.models import User
class Admin(User):
    __tablename__='admin'
    id=db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)

    __mapper_args__={'polymorphic_identity':'admin'}

