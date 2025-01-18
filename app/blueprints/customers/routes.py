# This file contains the routes related to Customers

# Imports
from flask import request, jsonify
from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema
from marshmallow import ValidationError
from app.models import Customer, db
from sqlalchemy import select, delete

# Create New Customer
@customers_bp.route("/", methods=['POST'])
def create_customer():
    try: 
		# Deserialize and validate input data
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
	# Use data to create an instance of Customer
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    
	# Save new_customer to the database
    db.session.add(new_customer)
    db.session.commit()

	# Use schema to return the serialized data of the created customer
    return customer_schema.jsonify(new_customer), 201

# Get Customers (all)
@customers_bp.route('/', methods=['GET'])
def get_customers():
    query = select(Customer)
    result = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(result), 200

# Get Customer (single)
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()
    
    if customer == None:
        return jsonify({"message": "invalid customer id"}), 400
    
    return customer_schema.jsonify(customer), 200

# Update Customer
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()
    
    if customer == None:
        return jsonify({"message": "invalid customer id"})

    try: 
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        setattr(customer, field, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

# Delete Customer
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted customer {customer_id}"})
