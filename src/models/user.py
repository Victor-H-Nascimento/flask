from bcrypt import gensalt, hashpw, checkpw

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
    activated = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

    def __init__(self, email: str, name: str, lastname: str, document: str, phone_number: str,  pwd: str, activated: bool = True):
        self.email = email
        self.name = name
        self.lastname = lastname
        self.document = document
        self.phone_number = phone_number
        self.pwd = hashpw(pwd.encode('utf-8'), gensalt()).decode('utf-8')
        self.activated = activated

    def verify_password(self, pwd):
        return checkpw(pwd.encode('utf-8'), self.pwd.encode('utf-8'))


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id",
                  "email",
                  "name",
                  "lastname"
                  )
