# This file is for token creation and validation

# Imports
import jose
from jose import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify
import os


# Creating a token signature
SECRET_KEY = os.environ.get('SQLALCHEMY_DATABASE_URI') or "big bad mama jama"

# Funtion to encode token
def encode_token(customer_id):
    # Payload = info packaged into token
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1), # Exiration
        'iat': datetime.now(timezone.utc), # Issued At
        'sub': str(customer_id) # Customer token belongs to
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256") # Creating token
    return token 

# Creating token verification wrapper for routes
def token_required(f): # f represents the function we are wrapping
    @wraps(f) # wrapping the function received with the decoration function below
    def decorated(*args, **kwargs): # adding functions to our wrapper with args and kwargs
        token = None # setting token == nothing

        if 'Authorization' in request.headers: # verifying authorization was requested
            
            # accessing token string using split() to remove 'Bearer' from the string
            token = request.headers['Authorization'].split()[1]

            # if no token return message to user
            if not token:
                return jsonify({'message': 'Missing token'}), 400
            
            # verify valid token & get customer_id
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
                print(data)
                customer_id = data['sub']

            # specified user message for expired token
            except jose.exceptions.ExpiredSignatureError:
                return jsonify({'message': 'Token expired'}), 400
            
            # specified user message for invalid token
            except jose.exceptions.JWTError:
                return jsonify({'message': 'Invalid token'}), 400
            
            # Pass customer_id as a keyword argument to the wrapped route function
            kwargs['customer_id'] = customer_id
        
        # if token not verified return message to user
        else:
            return jsonify({'message': 'You must be logged in to access this.'}), 400
        
        # Call the route function with the modified args and kwargs
        return f(*args, **kwargs)
      
    # return decorated(wrapped) function 
    return decorated