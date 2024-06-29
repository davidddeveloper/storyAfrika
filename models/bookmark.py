"""
    bookmark: represent the number of bookmarks for a story

"""

from models.base_model import BaseModel


class Bookmark(BaseModel):
    """ Represent a bookmark 
    
        - Attributes:
            - story_id: the story that was bookmarked
            - user_id: the user that bookmarkd the story
            - created_at: date and time it was created

    """

    def __init__(self, story_id, user_id):
        if isinstance(story_id, str) and isinstance(user_id, str):
            self.story_id = story_id
            self.user_id = user_id
        else:
            raise ValueError("arguments must be a string")
