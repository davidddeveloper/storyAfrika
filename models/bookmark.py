"""
    bookmark: represent the number of bookmarks for a story

"""

import os
from models.imports import *
from models.base_model import BaseModel, Base


class Bookmark(BaseModel, Base):
    """ Represent a bookmark

        - Attributes:
            - story_id: the story that was bookmarked
            - user_id: the user that bookmarkd the story
            - created_at: date and time it was created

    """

    if os.getenv('STORAGE') in ['db', 'DB']:
        __tablename__ = 'bookmarks'
        story_id = Column(String(60), ForeignKey('stories.id'), nullable=False)
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
