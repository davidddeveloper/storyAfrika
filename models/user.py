"""
    user: represent a model for creating users

"""
from models.base_model import BaseModel


class User(BaseModel):
    """
        Represents a user

        Attributes:
            - username: user identity on the platform
            - fullname: first name last name and any other name
            - email: user email address
            - password: password of the user
            - short_bio: who the user is
            - about: detail description of the user
    """

    def __init__(
            self, username, email, password, **kwargs
        ):
        super().__init__(self, **kwargs)

        arguments = {
            'username': username,
            'email': email,
            'password': password
        }
        for argument, value in arguments.items(): 
            if not isinstance(value, str):
                raise ValueError(f"{argument} must ba a string")
            
            setattr(self, argument, value)