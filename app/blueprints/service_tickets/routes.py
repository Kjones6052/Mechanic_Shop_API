# This file contains the routes related to Service Tickets

# Imports
from flask import request, jsonify
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema, return_service_ticket_schema, edit_service_ticket_schema, required_parts_schema
from marshmallow import ValidationError
from app.models import Service_Ticket, db, Mechanic, RequiredParts
from sqlalchemy import select
from app.extensions import limiter, cache
from app.utils.util import token_required

# New Service_Ticket
@service_tickets_bp.route("/", methods=['POST'])
# Limiting this route to reduce the amount of failed attempts a user can do to prevent excessive use of resources
@limiter.limit("3 per hour")
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
            return jsonify({"message": "Mechanic not found"}), 400
        
    db.session.add(new_service_ticket)
    db.session.commit()

    return return_service_ticket_schema.jsonify(new_service_ticket), 201

# Get Service_Tickets (all)
@service_tickets_bp.route('/', methods=['GET'])
# Cached list of customers to satisfy repetative requests faster
@cache.cached(timeout=60)
def get_service_ticket():
    query = select(Service_Ticket)
    result = db.session.execute(query).scalars().all() # execute query and assign to variable
    return service_tickets_schema.jsonify(result), 200 

# Get Service Tickets by Customer ID
@service_tickets_bp.route('/<int:customer_id>/my_tickets', methods=['GET'])
# Cached list of service tickets to satisfy repetative requests faster
@cache.cached(timeout=60)
@token_required # applying token verification wrapper to route
def get_customer_service_tickets(customer_id):
    query = select(Service_Ticket).where(Service_Ticket.customer_id == customer_id)
    customer_service_tickets = db.session.execute(query).scalars().all()

    if not customer_service_tickets:
        return jsonify({"message": "No customer service tickets found"}), 400
    
    return service_tickets_schema.jsonify(customer_service_tickets), 200

# Edit Service Ticket 
@service_tickets_bp.route('/<int:service_ticket_id>/edit', methods=['PUT'])
def edit_service_ticket(service_ticket_id):
    try:
        service_ticket_edits = edit_service_ticket_schema.load(request.json) # creating instance of edit service ticket schema
    except ValidationError as e:
        return jsonify(e.messages), 400 # if error return message to user display

    query = select(Service_Ticket).where(Service_Ticket.id == service_ticket_id) # create query to get service ticket according to id
    service_ticket = db.session.execute(query).scalars().first() # execute query and assign to variable

    # verify service ticket exists
    if not service_ticket:
        return jsonify({"message": "No service ticket found"}), 400

    for mechanic_id in service_ticket_edits['add_mechanic_ids']: # for each mechanic id input
        query = select(Mechanic).where(Mechanic.id == mechanic_id) # create query to get mechanic according to id
        mechanic = db.session.execute(query).scalars().first() # execute query and assign to variable

        # if there is a mechanic and it's not in the service ticket already add mechanic to service ticket
        if mechanic and mechanic not in service_ticket.mechanics: 
            service_ticket.mechanics.append(mechanic)

    for mechanic_id in service_ticket_edits['remove_mechanic_ids']: # for each mechanic id input
        query = select(Service_Ticket).where(Service_Ticket.id == mechanic_id) # create query to get mechanic according to id
        mechanic = db.session.execute(query).scalars().first() # execute query and assign to variable

        # if there is a mechanic and it is in the service ticket remove mechanic from service ticket
        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)

    db.session.commit() # commit changes to database
    return return_service_ticket_schema.jsonify(service_ticket), 200

# Add Part to Service Ticket 
@service_tickets_bp.route('/<int:service_ticket_id>/add_part', methods=['PUT'])
def add_required_parts(service_ticket_id):
    try:
        service_ticket_data = required_parts_schema.load(request.json) # creating instance of required parts schema
    except ValidationError as e:
        return jsonify(e.messages), 400 # if error return message to user display

    query = select(Service_Ticket).where(Service_Ticket.id == service_ticket_id) # create query to get service ticket according to id
    service_ticket = db.session.execute(query).scalars().first() # execute query and assign to variable

    # verify service ticket exists
    if not service_ticket:
        return jsonify({"message": "No service ticket found"}), 400
    
    add_part = RequiredParts(ticket_id=service_ticket.id, part_id=service_ticket_data['part_id'], quantity=service_ticket_data['quantity']) # get part data and assign to variable
    db.session.add(add_part) # add part to service ticket

    return return_service_ticket_schema.jsonify(service_ticket), 200