#!/usr/bin/python3

"""
    base_model: represents shared attributes for all other class
                in the models folder

"""
import uuid
import datetime


class BaseModel:
    """ represents the blueprint for other clases 

        Attributes:
            id - a string representing the uuid of the instance
            created_at - date and time the instance was created at
            updated_at - the date and time the instance was modify
        
    """

    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now() 
        self.updated_at = datetime.datetime.now()
