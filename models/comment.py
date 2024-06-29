"""
    comment: represent a comment made on a particular story
             by a particular user

"""

from models.base_model import BaseModel


class Comment(BaseModel):
    """ Represent a comment 
    
        Attributes:
            - comment: text represent the comment
            - story_id: the story the comment was made on
            - user_id: user who made the comment

    """

    def __init__(self, comment, story_id, user_id):
        super().__init__(self)
        arguments = {
            'comment': comment,
            'story_id': story_id,
            'user_id': user_id
        }
        for argument, value in arguments.items(): 
            if not isinstance(value, str):
                raise ValueError(f"{argument} must ba a string")
        
        setattr(self, argument, value)
