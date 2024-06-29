"""
    topic_follower: number of people that are following a topic

"""

from models.base_model import BaseModel
from uuid import uuid4


class TopicFollower(BaseModel):
    """ Represent the number of people that are following a topic 
    
        - Attributes:
            - id: uuid4 identifier
            - user_id: users id
            - topic_id: topic id
    """

    def __init__(self, user_id, topic_id):
        self.id = uuid4()
        if isinstance(user_id, str) and isinstance(topic_id, str):
            self.user_id = user_id
            self.topic_id = topic_id
        else:
            raise ValueError("arguments must be a string")