# This file contains the routes related to Parts

# Imports
from flask import request, jsonify
from app.blueprints.parts import parts_bp
from app.blueprints.parts.schemas import part_schema, parts_schema
from marshmallow import ValidationError
from app.models import Part, db
from sqlalchemy import select
from app.extensions import limiter, cache


# Add New Part
@parts_bp.route("/", methods=['POST'])
# Limiting this route to reduce the amount of failed attempts a user can do to prevent excessive use of resources
@limiter.limit("3 per hour")
def create_part():
    try: 
		# Deserialize and validate input data
        part_data = part_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
	# use data to create an instance of part
    new_part = Part(part_name=part_data['part_name'], price=part_data['price'])
    
	# save new_part to the database and commit changes
    db.session.add(new_part)
    db.session.commit()

	# Use schema to return the serialized data of the created part
    return part_schema.jsonify(new_part), 201

# Get Inventory (all)
@parts_bp.route('/', methods=['GET'])
# Cached list of parts to satisfy repetative requests faster
@cache.cached(timeout=60)
def get_parts():
    query = select(Part) # create query to get all parts
    result = db.session.execute(query).scalars().all() # execute query and assign to variable
    return parts_schema.jsonify(result), 200 # return parts data to user display according to schema

    
# Update Part in Inventory
@parts_bp.route('/<int:part_id>', methods=['PUT'])
def update_part(part_id):
    query = select(Part).where(Part.id == part_id) # create query to get part data
    part = db.session.execute(query).scalars().first() # execute query and assign to variable
    
    # if no part return message to user display
    if part == None: 
        return jsonify({"message": "invalid part id"}), 400

    try: 
        part_data = part_schema.load(request.json) # validate part data with schema
    except ValidationError as e:
        return jsonify(e.messages), 400 # if error return message to user display
    
    # assigning part attributes with part data
    for field, value in part_data.items():
        setattr(part, field, value)

    # commit changes to database and return part data
    db.session.commit()
    return part_schema.jsonify(part), 200

# Delete Part from Inventory
@parts_bp.route('/<int:part_id>', methods=['DELETE'])
def delete_part(part_id):
    part = db.session.get(Part, part_id) # get part 
    if part:
        db.session.delete(part) # detele part from database
        db.session.commit() # commit changes to database
        return jsonify({"message": f"succesfully deleted part {part_id}"}), 200
    return jsonify({"message": "part not found"}), 400
