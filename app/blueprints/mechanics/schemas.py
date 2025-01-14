# This file contains the schemas related to Mechanics

# Imports
from app.models import Mechanic
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# Mechanic Schema
class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
    
# Instantiating Schema(s)
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
