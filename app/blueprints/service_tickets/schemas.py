# This file contains the schemas related to Service Tickets

# Imports
from app.models import Service_Ticket
from app.extensions import ma
from marshmallow import fields


# Member Schema
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    customer = fields.Nested("CustomerSchema")
    mechanics = fields.Nested("MechanicSchema", many=True)
    class Meta:
        model = Service_Ticket
        fields = ('VIN', 'service_date', 'service_desc', 'customer_id', 'mechanic_ids')
    
# Instantiating Schema(s)
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_service_ticket_schema = ServiceTicketSchema(exclude=["customer_id"])