from flask import request, jsonify
from web_flask.api.v1.services.jwt_handler import decode_jwt
from functools import wraps

def check_jwt():
    # Gets token from request header and tries to get it's payload
    # Will raise errors if token is missing, invalid or expired 
    token = request.headers.get('Authorization')
    if not token:
        raise Exception('Missing access token')
    jwt = token.split('Bearer ')[1]
    try:
        return decode_jwt(jwt)
    except Exception as e:
        raise Exception(f'Invalid access token: {e}')

def auth_guard(f, role=None):
    @wraps(f)  # keep metadata about the wrapped function
    def wrapper(*args, **kwargs):
        # Authentication gate
        try:
            user_data = check_jwt()
        except Exception as e:
            return jsonify({"message": f'{e}', "status": 401}), 401
        # Authorization gate
        # if role and role not in user_data['roles']:
        #    return jsonify({"message": 'Authorization required.', "status": 403}), 403
        # Proceed to original route function
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
