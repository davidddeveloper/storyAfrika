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
        # creator = Column(String(60), ForeignKey("users.id"), nullable=False)
    else:
        name = ''
        description = ''

    def __init__(self, name, description=None, **kwargs):
        super().__init__(self, **kwargs)

        if isinstance(name, str):
            self.name = name
        else:
            raise ValueError(f"{name} must be a string")

        if description:
            self.description = description
