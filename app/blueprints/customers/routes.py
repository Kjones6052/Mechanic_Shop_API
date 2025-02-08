# This file contains the routes related to Customers

# Imports
from flask import request, jsonify
from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema, customer_login_schema
from marshmallow import ValidationError
from app.models import Customer, db
from sqlalchemy import select
from app.extensions import limiter
from app.utils.util import encode_token, token_required


# User Login Route
@customers_bp.route("/login", methods=["POST"])
def login():

    # get credentials and assign to variables
    try:
        credentials = customer_login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']

    # if error display to user
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email) # create query to get customer data
    customer = db.session.execute(query).scalars().first() # execute query and assign customer data to variable

    # if member & password are correct encode token for member
    if customer and customer.password == password:
        token = encode_token(customer.id)

        # define successful user message
        response = {
            "status": "success",
            "message": "successfully logged in",
            "token": token
        }

        return jsonify(response), 200 # return successful user message to user display
    else:
        return jsonify({"message": "invalid email or password"}), 400 # if error diplay to user


# Create New Customer
@customers_bp.route("/", methods=['POST'])
# Limiting this route to reduce the amount of failed attempts a user can do to prevent excessive use of resources
@limiter.limit("3 per hour")
def create_customer():
    try: 
		# Deserialize and validate input data
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
	# Use data to create an instance of Customer
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], password=customer_data['password'])
    
	# Save new_customer to the database
    db.session.add(new_customer)
    db.session.commit()

	# Use schema to return the serialized data of the created customer
    return customer_schema.jsonify(new_customer), 201

# Get Customers (all)
@customers_bp.route('/', methods=['GET'])
def get_customers():
    try:
        page = int(request.args.get('page')) # creating variable for page number
        per_page = int(request.args.get('per_page')) # creating variable for number per page
        query = select(Customer) # create query to get all customers
        result = db.session.execute(query, page=page, per_page=per_page) # execute query with parameters and assign to variable
        return customers_schema.jsonify(result), 200
    except:
        query = select(Customer) # create query to get all customers
        result = db.session.execute(query).scalars().all() # if try fails execute query assign to variable
        return customers_schema.jsonify(result), 200

# Get Customer (single)
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()
    
    if customer == None:
        return jsonify({"message": "customer not found"}), 400
    
    return customer_schema.jsonify(customer), 200

# Update Customer
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required # applying token verification wrapper to route
def update_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()
    
    if customer == None:
        return jsonify({"message": "customer not found"}), 400

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
@token_required # applying token verification wrapper to route
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted customer {customer_id}"}), 200
