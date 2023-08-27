from bcrypt import gensalt, hashpw, checkpw
from sqlalchemy.orm import relationship

from src import db, ma


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    document = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    pwd = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    number = db.Column(db.String(255), nullable=True)
    zip_code = db.Column(db.String(255), nullable=True)
    neighborhood = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    activated = db.Column(db.Boolean, nullable=False)

    pets = relationship("Pet", backref="pets")

    def __repr__(self):
        return f'<User {self.name}>'

    def __init__(self, email: str, name: str, lastname: str, document: str, phone_number: str,  pwd: str,
                    address: str, number: str, zip_code: str, neighborhood: str,
                    username: str, role: str = 'user', activated: bool = True):
        self.email = email
        self.name = name
        self.lastname = lastname
        self.document = document
        self.phone_number = phone_number
        self.pwd = hashpw(pwd.encode('utf-8'), gensalt()).decode('utf-8')
        self.address = address
        self.number = number
        self.zip_code = zip_code
        self.neighborhood = neighborhood
        self.username = username
        self.role = role
        self.activated = activated

    def verify_password(self, pwd):
        return checkpw(pwd.encode('utf-8'), self.pwd.encode('utf-8'))


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id",
                  "email",
                  "name",
                  "lastname",
                  "address",
                  "number",
                  "zip_code",
                  "neighborhood",
                  "role",
                  )
