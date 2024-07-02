"""
    db_storage: represent the mysql database storage
    orm: sqlalchemy

"""

from models.imports import *
from models.base_model import Base
from models.bookmark import Bookmark
from models.comment import Comment
from models.follower import Follower
from models.like import Like
from models.story import Story
from models.topic_follower import TopicFollower
from models.topic import Topic
from models.user import User

username = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
storage = os.getenv('STORAGE')

models_2_tables = {
    'bookmarks': Bookmark,
    'comments': Comment,
    'followers': Follower,
    'likes': Like,
    'stories': Story,
    'topic_followers': TopicFollower,
    'topics': Topic,
    'users': User
}


class DBStorage:
    """ Represent the mysql db storage

    """

    __engine = ''
    _session = ''
    __objects = {}
    # f'mysql://{username}:{password}@{host}/{db}'

    def __init__(self):
        self.__engine = create_engine(
            'mysql+mysqlconnector://root:root@localhost/test_db',
            echo=True
        )

    def all(self):
        """ Represent all data """
        return DBStorage.__objects

    def new(self, obj):
        """ Takes an object and adds it __objects """
        self._session.add(obj)

    def save(self):
        """ Reflect changes to the database """
        self._session.commit()

    def reload(self):
        """ Fetch all the data from the db """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine)
        self._session = scoped_session(session_factory)

        for cls in models_2_tables.values():
            for obj in self._session.query(cls).all():
                DBStorage.__objects[f'{cls.__name__}.{obj.id}'] = obj

    def close(self):
        """ Close the current session """
        self._session.close()
