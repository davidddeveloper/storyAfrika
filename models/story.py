#!/usr/bin/python3

"""
    story: represent a model for creating a story

"""
import sqlalchemy as sa
import sqlalchemy.orm as so
from models.imports import *
from models.base_model import BaseModel, Base
from models.image_upload import ImageUpload


class Story(BaseModel, ImageUpload, Base):
    """ Represents a story

         Attributes:
            - title: short text representing the title
            - text: the actual text content of the story
            - user_id: id of the user that made the post
            - category_id: id of the category the post is under

    """

    if os.getenv('STORAGE') in ['db', 'DB']:
        __tablename__ = 'stories'
        title = Column(String(200), nullable=False)
        text = Column(Text, nullable=False)
        user_id = Column('User', ForeignKey('users.id'), nullable=False)

        comments = relationship('Comment', backref='story', lazy=True)
        likes = relationship('Like', backref='story', lazy=True)
        bookmarks = relationship('Bookmark', backref='story', lazy=True)
        image = Column(String(100), nullable=True) # path to image

    else:
        title = ''
        text = ''
        user_id = ''

    def to_dict(self):
        """ Dictionary representation of the object """

        dictionary = super().to_dict()
        dictionary['writer'] = self.writer.to_dict()
        dictionary['comments_count'] = len(self.comments)
        dictionary['likes_count'] = len(self.likes)
        dictionary['bookmarks_count'] = len(self.bookmarks)
        dictionary['read_time'] = self.read_time

        return dictionary

    @property
    def read_time(self):
        num_of_words = len(self.text.split())
        read_time_in_minutes = int(num_of_words / 225)

        return read_time_in_minutes

    @property
    def plain_text(self):
        import re, json

        if self.text and re.search(r'^\[', self.text):
            return json.dumps([content['content'].replace('⇅', '') for content in json.loads(re.sub('<[^>]+>', '', self.text)) 
                if content['content'] != '⇅']).replace('"', '').replace('[', '').replace(']','').replace("'", '')

        return self.text

    @property
    def newest_comments(self):
        """ order comments based on newest first """
        from models.comment import Comment

        return (
            Comment.newest().where(Comment.story_id == self.id)
        )

    @property
    def relevant_comments(self):
        """ compute relevant comments base on number of likes """
        from models.comment import Comment
        from models.comment_like import CommentLike
        from models.comment_unlike import CommentUnLike

        likes_count = (
            sa.select(sa.func.count(CommentLike.id))
            .where(CommentLike.comment_id == Comment.id)
            .scalar_subquery()
        )

        unlikes_count = (
            sa.select(sa.func.count(CommentUnLike.id))
            .where(CommentUnLike.comment_id == Comment.id)
            .scalar_subquery()
        )

        return (
            sa.select(Comment)
            .join(Story)
            .where(Comment.story_id == self.id)
            .order_by(sa.desc(likes_count - unlikes_count))
        )


    def __init__(self, title, text, user_id, **kwargs):
        super().__init__(**kwargs)

        arguments = {
            'title': title,
            'text': text,
            'user_id': user_id,
        }
        for argument, value in arguments.items():
            if not isinstance(value, str):
                raise ValueError(f"{argument} must ba a string")

            setattr(self, argument, value)
