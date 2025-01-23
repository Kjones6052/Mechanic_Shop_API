# This file contains the schemas related to Service Tickets

# Imports
from app.models import Service_Ticket, RequiredParts
from app.extensions import ma
from marshmallow import fields

# service ticket Schema
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket
        fields = ('VIN', 'service_date', 'service_desc', 'customer_id', 'mechanic_ids')
        include_relationships = True
    required_parts = fields.Nested("RequiredPartsSchema", exclude=["id"], many=True)
    customer = fields.Nested("CustomerSchema")
    mechanics = fields.Nested("MechanicSchema", many=True)
    
#  edit service ticket schema
class EditServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")

# required parts schema
class RequiredPartsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RequiredParts
    part = fields.Nested("PartSchema")

# Instantiating Schema(s)
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_service_ticket_schema = ServiceTicketSchema(exclude=["customer_id"])
edit_service_ticket_schema = EditServiceTicketSchema()
required_parts_schema = RequiredPartsSchema()