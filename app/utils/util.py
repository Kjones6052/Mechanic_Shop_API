# This file is for token creation and validation

# Imports
import jose
from jose import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify
from urllib.request import urlopen
import json
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
                return jsonify({'message': 'missing token'}), 401
            
            # verify valid token & get customer_id
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
                print(data)
                customer_id = data['sub']

            # specified user message for expired token
            except jose.exceptions.ExpiredSignatureError:
                return jsonify({'message': 'token expired'}), 401
            
            # specified user message for invalid token
            except jose.exceptions.JWTError:
                return jsonify({'message': 'invalid token'}), 401
            
            # Pass customer_id as a keyword argument to the wrapped route function
            kwargs['customer_id'] = customer_id
        
        # if token not verified return message to user
        else:
            return jsonify({'message': 'you must be logged in to access this.'}), 401
        
        # Call the route function with the modified args and kwargs
        return f(*args, **kwargs)
      
    # return decorated(wrapped) function 
    return decorated


# Auth0 Verification and Use
AUTH0_DOMAIN = "Auth0 App Domain"
API_IDENTIFIER = "MSAPI000001"
ALGORITHMS = ["RS256"]

# Auth0 Token Verification
def verify_token(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    for key in jwks["keys"]:
        if key["kidd"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    issuer=f"https://{AUTH0_DOMAIN}/",
                )
                print('PAYLOAD:', payload) # used for testing errors
                return payload
            except jwt.ExpiredSignatureError:
                raise ValueError("Token is expired.")
            except jwt.JWTClaimsError:
                raise ValueError("Incorrect claims. Check the audience and issuer.")
            except Exception:
                raise ValueError("Unable to parse authentication token.")
        raise ValueError("No matching RSA key.")

def auth_token_required(f):
    def auth_decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", None)
        if not auth:
            return jsonify({"message": "Authorization header is missing"}), 401
        
        if "Bearer" not in auth:
            return jsonify({"message": "Bearer <Token> required."}), 401

        try:
            token = auth.split()[1]
            payload = verify_token(token) # used for testing errors
        except ValueError as e:
            return jsonify({"message": str(e)}), 401
        
        return f(payload, *args, **kwargs)
    
    return auth_decorated

# example of protected route will be removed later
# @app.route("/protected", methods=["GET"])
# @auth_token_required
# def protected(payload):
#     return jsonify({"message": "You accessed a protected route!", "customer":payload})