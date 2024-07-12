"""
    comment: represent a comment made on a particular story
             by a particular user

"""

import uuid
import os
from models.imports import *
from models.base_model import BaseModel, Base


class Comment(BaseModel, Base):
    """ Represent a comment

        Attributes:
            - comment: text represent the comment
            - story_id: the story the comment was made on
            - user_id: user who made the comment

    """

    if os.getenv('STORAGE') in ['db', 'DB']:
        __tablename__ = 'comments'
        id = Column(String(60), primary_key=True, default=str(uuid.uuid4()))
        comment = Column(Text, nullable=False)
        story_id = Column('Story', ForeignKey('stories.id'), nullable=False)
        user_id = Column('User', ForeignKey('users.id'), nullable=False)

    else:
        comment = ''
        story_id = ''
        user_id = ''

    def __init__(self, comment, story_id, user_id, **kwargs):
        super().__init__(**kwargs)
        arguments = {
            'comment': comment,
            'story_id': story_id,
            'user_id': user_id
        }
        for argument, value in arguments.items():
            if not isinstance(value, str):
                raise ValueError(f"{argument} must ba a string")

            setattr(self, argument, value)
