"""
    topic: represent a topic a story fall under

"""

from models.base_model import BaseModel


class Topic(BaseModel):
    """ Represent a topic 
    
        
    """

    def __init__(self, name, description=None):
        super().__init__(self)

        if isinstance(name, str):
            self.name = name
        else:
            raise ValueError(f"{name} must be a string")

        if description:
            self.description = description
