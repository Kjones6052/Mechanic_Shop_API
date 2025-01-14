# This file contains the routes related to Mechanics

# Imports
from flask import request, jsonify
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError
from app.models import Mechanic, db
from sqlalchemy import select, delete


# New Mechanic
@mechanics_bp.route("/", methods=['POST'])
def create_mechanic():
    try: 
		# Deserialize and validate input data
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
	# use data to create an instance of Mechanic
    new_mechanic = Mechanic(name=mechanic_data['name'], email=mechanic_data['email'], phone=mechanic_data['phone'], salary=mechanic_data['salary'])
    
	# save new_mechanic to the database
    db.session.add(new_mechanic)
    db.session.commit()

	# Use schema to return the serialized data of the created Mechanic
    return mechanic_schema.jsonify(new_mechanic), 201

# Get Mechanics (all)
@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    result = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(result), 200 
    
# Update Mechanic
@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()
    
    if mechanic == None:
        return jsonify({"message": "invalid mechanic id"})

    try: 
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in mechanic_data.items():
        setattr(mechanic, field, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

# Delete Mechanic
@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    query = delete(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query)

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted mechanic {mechanic_id}"})


