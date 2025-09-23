from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    firstname =  db.Column(db.String(50), nullable=False, unique=True)
    lastname =  db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    role=db.Column(db.String(50))

    __mapper_args__={
        'polymorphic_on':role,
        'polymorphic_identity':'user'
    }


    def __init__(self, firstname, lastname, password, role):
        self.firstname = firstname
        self.lastname = lastname
        self.set_password(password)
        self.role=role

    def get_json(self):
        return{
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"|{self.username}({self.type})|"
