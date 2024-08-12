"""
    follower: represents a followers

"""

from models.imports import *
from models.base_model import BaseModel, Base


class Follower(BaseModel, Base):
    """ Represent a follower

        Attributes:
            - follower_id: the user id
            - followed_id: the person following the user
    """

    if os.getenv('STORAGE') in ['db', 'DB']:
        __tablename__ = 'followers'
        follower_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
        followed_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    else:
        follower_id = ''
        followed_id = ''

    def __init__(self, follower_id, followed_id):
        super().__init__()
        if isinstance(follower_id, str) and isinstance(followed_id, str):
            self.follower_id = follower_id
            self.followed_id = followed_id
        else:
            raise ValueError("arguments must be a string")
