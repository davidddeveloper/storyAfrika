"""
    like: represent the number of likes for a story

"""

from models.imports import *
from models.base_model import BaseModel, Base


class Like(BaseModel, Base):
    """ Represent a like

        - Attributes:
            - story_id: the story that was liked
            - user_id: the user that liked the story
            - created_at: date and time it was created

    """

    if os.getenv('STORAGE') in ['db', 'DB']:
        __tablename__ = 'likes'
        story_id = Column(String(60), ForeignKey('stories.id', ondelete='CASCADE'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        story_id = ''
        user_id = ''

    def __init__(self, story_id, user_id):
        super().__init__()
        if isinstance(story_id, str) and isinstance(user_id, str):
            self.story_id = story_id
            self.user_id = user_id
        else:
            raise ValueError("arguments must be a string")
