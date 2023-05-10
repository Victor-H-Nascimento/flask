from src.models.user import User
from src import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
