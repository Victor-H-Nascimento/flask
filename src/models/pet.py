from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src import db, ma

class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.String(255), nullable=False)
    breed = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(255), nullable=False)
    castrated = db.Column(db.Boolean, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    specie = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    activated = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Text(), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)

    timeline = relationship("Timeline", backref="timeline")

    def __init__(self, name: str, size: str, breed: str, age: str, castrated: bool,
                weight: float, specie: str, gender: str, user_id: int, description: str, activated: bool = True):
        self.name = name
        self.size = size
        self.breed = breed
        self.age = age
        self.castrated = castrated
        self.weight = weight
        self.specie = specie
        self.gender = gender
        self.user_id = user_id
        self.description = description
        self.activated = activated


class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet
        fields = ("id",
                  "name",
                  "size",
                  "breed",
                  "age",
                  "castrated",
                  "weight",
                  "specie",
                  "gender",
                  "description",
                  )
