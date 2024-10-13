"""
    topic: represent a topic a story fall under

"""

from models.image_upload import ImageUpload
from models.imports import *
from models.base_model import BaseModel, Base

if os.getenv('STORAGE') in ['db', 'DB']:
    story_topic_association = Table(
        'story_topic_association',
        Base.metadata,
        Column(
            'story_id', String(60), ForeignKey('stories.id'), primary_key=True
        ),
        Column(
            'topic_id', String(60), ForeignKey('topics.id'), primary_key=True
        )
    )
    topic_user_association = Table(
        'topic_user_association',
        Base.metadata,
        Column(
            'user_id', String(60), ForeignKey('users.id'), primary_key=True
        ),
        Column(
            'topic_id', String(60), ForeignKey('topics.id'), primary_key=True
        )
    )


class Topic(BaseModel, ImageUpload, Base):
    """ Represent a topic


    """

    if os.getenv('STORAGE') in ['db', 'DB']:
        __tablename__ = 'topics'
        name = Column(String(80), nullable=False)
        description = Column(String(200), nullable=True)
        banner = Column(String(100), nullable=True) # path to image
        stories = relationship(
            'Story',
            secondary=story_topic_association,
            backref='topics', lazy=True
        )
        followers = relationship('TopicFollower', backref='topic', lazy=True)

        contributors = relationship('User', secondary=topic_user_association, backref='topics', lazy=True)
        creator = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    else:
        name = ''
        description = ''

    def to_dict(self):
        """ Dictionary representation of the object """

        dictionary = super().to_dict()
        dictionary['stories'] = ''


        return dictionary

    def __init__(self, name, description=None, **kwargs):
        super().__init__(self, **kwargs)

        if isinstance(name, str):
            self.name = name
        else:
            raise ValueError(f"{name} must be a string")

        if description:
            self.description = description

    @classmethod
    def search_topics_by_title(cls, data):
        """
            search topics by title
        """
        from models.engine import storage

        return storage._session.query(cls).where(cls.name.contains(data))
