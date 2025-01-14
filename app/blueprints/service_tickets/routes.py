# This file contains the routes related to Service Tickets

# Imports
from flask import request, jsonify
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema, return_service_ticket_schema
from marshmallow import ValidationError
from app.models import Service_Ticket, db, Mechanic
from sqlalchemy import select


# New Service_Ticket
@service_tickets_bp.route("/", methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = Service_Ticket(VIN=service_ticket_data['VIN'], service_date=service_ticket_data['service_date'], service_desc=service_ticket_data['service_desc'], customer_id=service_ticket_data['customer_id'])
    
    for mechanic_id in service_ticket_data["mechanic_ids"]:
        query = select(Mechanic).where(Mechanic.id==mechanic_id)
        mechanic = db.session.execute(query).scalar()
        if mechanic:
            new_service_ticket.mechanics.append(mechanic)
        else:
            return jsonify({"message": "invalid mechanic id"})
        
    db.session.add(new_service_ticket)
    db.session.commit()

    
    return return_service_ticket_schema.jsonify(new_service_ticket), 201

# Get Service_Tickets (all)
@service_tickets_bp.route('/', methods=['GET'])
def get_service_ticket():
    query = select(Service_Ticket)
    result = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(result), 200 
