from bcrypt import gensalt, hashpw, checkpw
from sqlalchemy import ForeignKey

from src import db, ma

class Vet(db.Model):
    __tablename__ = 'vets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    pwd = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    activated = db.Column(db.Boolean, nullable=False)
    clinica_id = db.Column(db.Integer, ForeignKey('clinicas.id'), nullable=False)

    def __init__(self, name: str, username: str, pwd: str, clinica_id: int, role: str = 'vet', activated: bool = True):
        self.name = name
        self.username = username
        self.pwd = hashpw(pwd.encode('utf-8'), gensalt()).decode('utf-8')
        self.clinica_id = clinica_id
        self.role = role
        self.activated = activated
    
    def verify_password(self, pwd):
        return checkpw(pwd.encode('utf-8'), self.pwd.encode('utf-8'))


class VetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vet
        fields = ("id",
                  "name",
                  "role",
                  "clinica_id",
                  "username",
                  )
