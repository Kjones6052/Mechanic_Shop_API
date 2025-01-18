# This file contains the schemas related to Mechanics

# Imports
from app.models import Mechanic
from app.extensions import ma

# Mechanic Schema
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
    
# Instantiating Schema(s)
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
