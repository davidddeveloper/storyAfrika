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

    def all(self, cls=None):
        """ all objects

            Attributes:
                - cls: an optional class name
        """

        if cls is not None:
            objs = {}
            for key, obj in self.__objects.items():
                try:
                    if obj.to_dict()['__class__'] == cls.__name__:
                        objs[key] = obj
                except Exception:
                    return objs

            return objs

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
                {x: y.to_dict() for x, y in FileStorage.__objects.items()},
                fi
            )

    def reload(self):
        """ Load the data from the storage """

        if not os.path.exists('file.json'):
            return

        with open(FileStorage.__filename, 'r') as fi:
            data = json.load(fi)

            for key, values in data.items():

                FileStorage.__objects[key] = FileStorage.__classes.get(
                    values.get('__class__')
                )(**values)

    def delete(self, obj=None):
        """ Deletes an object

            Attributes:
                - obj: the object to be deleted
        """

        if obj is not None:
            self.__objects.pop(f'{obj.__class__.__name__}.{obj.id}', None)

    def get(self, cls=None, id=None):
        """ Get a specific object

        Attributes:
            - cls: the class
            - id: the uuid of the object
        """

        if cls is None or id is None:
            return None
        try:
            instance = self.__objects.get(f'{cls.__name__}.{id}')

        except Exception:
            pass

        return instance
