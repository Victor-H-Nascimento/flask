from bcrypt import gensalt, hashpw, checkpw
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from src import db, ma
from src.models.services import ServicesSchema

clinicas_services = db.Table("clinicas_services",
                                 db.Column("clinicas_id", ForeignKey("clinicas.id")),
                                 db.Column("services_id", ForeignKey("services.id")))


class Clinica(db.Model):
    __tablename__ = 'clinicas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(255), nullable=False)
    neighborhood = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    pwd = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    activated = db.Column(db.Boolean, nullable=False)

    services = relationship("Services", secondary=clinicas_services, backref="clinica")

    vets = relationship("Vet", backref="vets")

    def __repr__(self):
        return f'<Clinica {self.name}>'

    def __init__(self, name: str, cnpj: str, address: str, number: str, zip_code: str,  neighborhood: str,
                    username: str, pwd: str, role: str = 'clinica', activated: bool = True):
        self.name = name
        self.cnpj = cnpj
        self.address = address
        self.number = number
        self.zip_code = zip_code
        self.neighborhood = neighborhood
        self.username = username
        self.pwd = hashpw(pwd.encode('utf-8'), gensalt()).decode('utf-8')
        self.role = role
        self.activated = activated

    def verify_password(self, pwd):
        return checkpw(pwd.encode('utf-8'), self.pwd.encode('utf-8'))


class ClinicaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Clinica
        fields = ("id",
                  "name",
                  "cnpj",
                  "address",
                  "number",
                  "zip_code",
                  "neighborhood",
                  "role",
                  "services",
                  )
    services = ma.List(ma.Nested(ServicesSchema))
