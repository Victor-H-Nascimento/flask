from datetime import datetime
from sqlalchemy import ForeignKey

from src import db, ma

class Timeline(db.Model):
    __tablename__ = 'timeline'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    title = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    vet = db.Column(db.String(255), nullable=False)
    clinic = db.Column(db.String(255), nullable=False)
    activated = db.Column(db.Boolean, nullable=False)
    pet_id = db.Column(db.Integer, ForeignKey('pets.id'), nullable=False)

    def __init__(self, type: str, title: str, description: str, \
                  vet: str, clinic: str, pet_id: int, activated: bool = True):
        self.type = type
        self.title = title
        self.created_date = datetime.today()
        self.description = description
        self.vet = vet
        self.clinic = clinic
        self.pet_id = pet_id
        self.activated = activated


class TimelineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Timeline
        fields = ("id",
                  "type",
                  "title",
                  "created_date",
                  "description",
                  "vet",
                  "clinic",
                  "pet_id",
                  )
