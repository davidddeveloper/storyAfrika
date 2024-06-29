#!/usr/bin/python3

"""
    story: represent a model for creating a story

"""
from models.base_model import BaseModel


class Story(BaseModel):
    """ Represents a story 

         Attributes:
            - title: short text representing the title
            - text: the actual text content of the story
            - user_id: id of the user that made the post
            - category_id: id of the category the post is under

    """

    def __init__(self, title, text, user_id, topics_id):
        super().__init__(self)

        arguments = {
            'title': title,
            'text': text,
            'user_id': user_id,
            'topics_id': topics_id
        }
        for argument, value in arguments.items(): 
            if argument == 'topics_id' and not isinstance(value, list):
                raise ValueError(f"{argument} must ba a list")
            
            elif argument != 'topics_id' and not isinstance(value, str):
                raise ValueError(f"{argument} must ba a string")
            
            # check if value inside topics_id list is all string
            # otherwise raise a value error
            for idx, id_val in enumerate(topics_id):
                if type(id_val) != str:
                    raise ValueError(
                        f"{id_val} at index {id_val} in topics_id must be a string"
                    )
            
            
            setattr(self, argument, value)
        
        
      
