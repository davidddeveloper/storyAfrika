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

        if kwargs:
            for key, val in kwargs.items():
                if key != '__class__':
                    setattr(self, key, val)
            
            if 'id' in kwargs and kwargs.get('id') is str:
                self.id = kwargs.get('id')
            else:
                self.id = str(uuid.uuid4())
            
            if 'created_at' in kwargs and isinstance(kwargs.get('created_at'), str):
                self.created_at = datetime.datetime.fromisoformat(
                    kwargs.get('created_at')
                )
            else:
                self.created_at = datetime.datetime.now() 

            if 'updated_at' in kwargs and isinstance(kwargs.get('updated_at'), str):
                self.updated_at = datetime.datetime.fromisoformat(
                    kwargs.get('updated_at')
                )
            else:
                self.updated_at = datetime.datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
    
    def to_dict(self):
        """ Dictionary representation of the object """

        dictionary = self.__dict__.copy()
        dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        dictionary['created_at'] = dictionary['created_at'].isoformat()
        dictionary['__class__'] = self.__class__.__name__

        return dictionary
    
    def __str__(self) -> str:
        return f"[{self.__class__.__name__}.{self.id}] {self.to_dict()}"

    def save(self):
        """ write the object to storage """
        from models.engine import storage

        storage.new(self)
        self.updated_at = datetime.datetime.now()
        storage.save()
        
        