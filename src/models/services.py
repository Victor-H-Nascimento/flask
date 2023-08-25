from src import db, ma

class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    activated = db.Column(db.Boolean, nullable=False)

    def __init__(self, name: str, activated: bool = True):
        self.name = name
        self.activated = activated


class ServicesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Services
        fields = ("id",
                  "name",
                  )
