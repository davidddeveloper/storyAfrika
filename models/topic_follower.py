"""
    topic_follower: number of people that are following a topic

"""

from uuid import uuid4
from models.imports import *
from models.base_model import BaseModel, Base


class TopicFollower(BaseModel, Base):
    """ Represent the number of people that are following a topic

        - Attributes:
            - id: uuid4 identifier
            - user_id: users id
            - topic_id: topic id
    """

    if os.getenv('STORAGE') in ['db', 'DB']:
        __tablename__ = 'topic_followers'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        topic_id = Column(String(60), ForeignKey('topics.id'), nullable=False)
    else:
        user_id = ''
        topic_id = ''

    def __init__(self, user_id, topic_id):
        if isinstance(user_id, str) and isinstance(topic_id, str):
            self.user_id = user_id
            self.topic_id = topic_id
        else:
            raise ValueError("arguments must be a string")
