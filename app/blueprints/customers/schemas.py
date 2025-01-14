# This file contains the schemas related to Customers

# Imports
from app.models import Customer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
    
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)