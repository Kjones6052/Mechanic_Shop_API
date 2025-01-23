# This file contains the schemas related to Customers

# Imports
from app.models import Customer
from app.extensions import ma


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer # basing schema on Customer Table Model
    

# instantiating schemas
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Creating a login schema that excludes details name, phone for customer authentication
customer_login_schema = CustomerSchema(exclude=['name', 'phone'])