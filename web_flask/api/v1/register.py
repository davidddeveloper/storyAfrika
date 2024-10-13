from flask import request, jsonify
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import check_for_valid_json
from web_flask.api.v1.helper_func import validate_username
from web_flask.api.v1.helper_func import validate_email
from models.user import User
from models.role import Role
from models.engine import storage
from web_flask.api.v1.services.data_service import get_user_data


@views.route(
    'users/register/',
    strict_slashes=False,
    methods=['POST']
)
def register_user():
    """ creates a user """
    # checks for valid json
    try:
        user_json = request.get_json()
        property = check_for_valid_json(user_json, ['username', 'email', 'password'])
        if property:
            return jsonify({"Error": f"Missing field: {property}"})

    except Exception:
        return jsonify({"Error": 'not a valid json'}), 400

    else:
        if not validate_username(user_json['username']):
            return jsonify(
                {"Error": 
                    {
                    "type":"username",
                    "message": "a user with this username already exists",
                    "username": f"{user_json['username']}"}
                    }
                )
        if not validate_email(user_json['email']):
            return ({"Error": 
                    {
                    "type":"email",
                    "message": "a user with this email already exists",
                    "email": f"{user_json['email']}"}
                    }
            )
        if isinstance(user_json, dict):
            user = User(
                    username=user_json['username'],
                    email=user_json['email'],
                    password=user_json['password']
                )
        if isinstance(user_json, list):
            user = User(
                username=user_json[0],
                email=user_json[1],
                password=user_json[2]
            )
        
        # set password hashes
        user.set_password(user.password)

        # generate an image base on initial
        user.set_default_profile()

        role = storage._session.query(Role).where(Role.role == 'user').first()

        if not role:
            role = Role(role='user')
            role.save()

        user.save()
        user.roles.append(role)
        user.save()
        storage.save()
        print(user)
        return jsonify(user.to_dict()), 201
