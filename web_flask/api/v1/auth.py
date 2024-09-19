from flask import jsonify, request
from web_flask.api.v1 import views
from web_flask.api.v1.services.auth_provider import authenticate
from web_flask.api.v1.services.jwt_handler import generate_jwt


@views.route('/auth/', methods=['POST'], strict_slashes=False)
def auth():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({"message": "Email or password missing", "status": 400}), 400

    user_data = authenticate(email, password)
    if not user_data:
        return jsonify({'user': user_data, "message": "Invalid credentials", "status": 400}), 400


    token = generate_jwt(payload=user_data, lifetime=60) # <--- generates a JWT with valid within 1 hour by now

    return jsonify({"data": token, "status": 200}), 200

