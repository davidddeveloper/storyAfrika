"""
    follower: represents a followers

"""
from models.base_model import BaseModel


class Follower(BaseModel):
    """ Represent a follower 
    
        Attributes:
            - follower_id: the user id
            - followed_id: the person following the user
    """


    def __init__(self, follower_id, followed_id):
        super().__init__(self)
        if isinstance(follower_id, str) and isinstance(followed_id, str):
            self.follower_id = follower_id
            self.followed_id = followed_id
        else:
            raise ValueError("arguments must be a string")