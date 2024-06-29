"""
    file_storage: represents the structure for storing data as json in a file

"""
import os
import json

from models.base_model import BaseModel
from models.story import Story
from models.comment import Comment
from models.user import User
from models.topic import Topic
from models.like import Like
from models.bookmark import Bookmark
from models.follower import Follower
from models.topic_follower import TopicFollower



class FileStorage:
    """ Represent file storage 
    
    """

    __objects = {}  # class.instanceid: instance
    __filename = 'file.json'
    __classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Comment': Comment,
        'Story': Story,
        'Topic': Topic,
        'TopicFollower': TopicFollower,
        'Like': Like,
        'Bookmark': Bookmark,
        'Follower': Follower
        
    }

    def all(self):
        """ all objects """

        return FileStorage.__objects
    
    def new(self, obj):
        """ Takes an object adds it to __object """

        FileStorage.__objects[
            f'{obj.__class__.__name__}.{obj.id}'
        ] = obj
    
    def save(self):
        """ write the a modify data in __objects to a file """

        with open(FileStorage.__filename, 'w') as fi:
            
            json.dump(
                {x:y.to_dict() for x,y in FileStorage.__objects.items()},
                fi
            )

    def reload(self):
        """ Load the data from the storage """

        with open(FileStorage.__filename, 'r') as fi:
            data = json.load(fi)

            print(data)
            for key, values in data.items():
                print(values)
                FileStorage.__objects[key] = FileStorage.__classes.get(values.get('__class__'))(**values)
