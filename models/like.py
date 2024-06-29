"""
    like: represent the number of likes for a story

"""

from models.base_model import BaseModel


class Like(BaseModel):
    """ Represent a like 
    
        - Attributes:
            - story_id: the story that was liked
            - user_id: the user that liked the story
            - created_at: date and time it was created

    """

    def __init__(self, story_id, user_id):
        super().__init__(self)
        if isinstance(story_id, str) and isinstance(user_id, str):
            self.story_id = story_id
            self.user_id = user_id
        else:
            raise ValueError("arguments must be a string")

