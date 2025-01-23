# This file is for the schemas related to Parts (Inventory)

# Imports
from app.models import Part
from app.extensions import ma

# Part Schema
class PartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Part # basing schema on Part (Inventory) Table Model
    
# Instantiating Schema(s)
part_schema = PartSchema()
parts_schema = PartSchema(many=True)