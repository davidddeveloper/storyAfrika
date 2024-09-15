"""
    comment: represent a comment made on a particular story
             by a particular user

"""

import sqlalchemy as sa

import os
from models.imports import *
from models.base_model import BaseModel, Base
from models.comment_like import CommentLike
from models.comment_unlike import CommentUnLike


class Comment(BaseModel, Base):
    """ Represent a comment

        Attributes:
            - comment: text represent the comment
            - story_id: the story the comment was made on
            - user_id: user who made the comment

    """

    if os.getenv('STORAGE') in ['db', 'DB']:
        __tablename__ = 'comments'
        comment = Column(Text, nullable=False)
        story_id = Column(String(60), ForeignKey('stories.id', ondelete='CASCADE'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False,)
        likes = relationship('CommentLike', backref='comment', lazy=True, passive_deletes=True, cascade='all, delete-orphan')
        unlikes = relationship('CommentUnLike', backref='comment', lazy=True, passive_deletes=True, cascade='all, delete-orphan')

    else:
        comment = ''
        story_id = ''
        user_id = ''

    def to_dict(self):
        """ Dictionary representation of the object """
        from models.engine import storage

        dictionary = super().to_dict()

        dictionary['commenter'] = self.commenter.to_dict()
        dictionary['likes_count'] = storage._session.execute(self.likes_count).scalar()
        dictionary['unlikes_count'] = storage._session.execute(self.unlikes_count).scalar()

        return dictionary

    def __init__(self, comment, story_id, user_id, **kwargs):
        super().__init__(**kwargs)
        arguments = {
            'comment': comment,
            'story_id': story_id,
            'user_id': user_id
        }
        for argument, value in arguments.items():
            if not isinstance(value, str):
                raise ValueError(f"{argument} must ba a string")

            setattr(self, argument, value)
    
    @classmethod
    def relevant(cls):
        """ compute relevant comments base on number of likes """
        from models.engine import storage
        from models.story import Story
        comments = storage._session.execute(sa.select(Comment).join(Story).scalars().all())
        #return (
        #    sa.select(cls)
        #    .join(Story)
        #    .add_columns(
        #    ).order_by(
        #        (cls.likes_count() - cls.unlikes_count()).desc()
        #    )
        #)

        return (
            sorted(
                comments,
                key=lambda comment: comment.likes_count - comment.unlikes_count,
                reverse=True
            )
        )
    
    @classmethod
    def newest(cls):
        """ order comments based on newest first """

        return (
            sa.select(cls).order_by(cls.created_at.desc())
        )

    def like(self, user_id):
        """ like a comment 
        
            Attribute:
                - user_id: the id of the user that wants to like a comment

        """

        from models.engine import storage

        query = storage._session.query(CommentUnLike).where(sa.and_(
            CommentUnLike.user_id == user_id,  # get only the comments that the user has liked
            CommentUnLike.comment_id == self.id
        ))
        if storage._session.execute(query).scalar_one_or_none():
            comment = storage._session.execute(query).scalar()
            comment.delete()

        comment_like = CommentLike(comment_id=self.id, user_id=user_id)
        comment_like.save()



        return 'liked'

    def unlike(self, user_id):
        """ like a comment 

            Attribute:
                - user_id: the id of the user that wants to like a comment

        """
        from models.engine import storage

        query = storage._session.query(CommentLike).where(sa.and_(
            CommentLike.user_id == user_id,  # get only the comments that the user has liked
            CommentLike.comment_id == self.id
        ))
        if storage._session.execute(query).scalar_one_or_none():
            comment = storage._session.execute(query).scalar()
            comment.delete()

        comment_unlike = CommentUnLike(comment_id=self.id, user_id=user_id)
        comment_unlike.save()

        return 'unliked'

    def is_liked_by(self, user_id):
        """ check if a user is liking a comment 
        
            Attributes:
                - user_id: the id of the user

        """
        from models.engine import storage

        # comment_like = sa.select(Comment).join(CommentLike).where(sa.and_(  # combine comment and commentlike
        #    CommentLike.user_id == user_id,  # get only the comments that the user has liked
        #    self.id == CommentLike.comment_id
        #))
        comment_like = sa.select(CommentLike).where(sa.and_(
            CommentLike.user_id == user_id,  # get only the comments that the user has liked
            CommentLike.comment_id == self.id
        ))

        result = storage._session.execute(comment_like).scalar_one_or_none()
        return result is not None

    def is_unliked_by(self, user_id):
        """ check if a user is unliking a comment 
        
            Attributes:
                - user_id: the id of the user

        """
        from models.engine import storage
        from models.comment_unlike import CommentUnLike

        # comment_like = sa.select(Comment).join(CommentLike).where(sa.and_(  # combine comment and commentlike
        #    CommentLike.user_id == user_id,  # get only the comments that the user has liked
        #    self.id == CommentLike.comment_id
        #))
        comment_unlike = storage._session.query(CommentUnLike).where(sa.and_(
            CommentUnLike.user_id == user_id,  # get only the comments that the user has liked
            CommentUnLike.comment_id == self.id
        ))

        result = storage._session.execute(comment_unlike).scalar_one_or_none()
        return result is not None
        
    @property
    def likes_count(self):
        """ count the number of likes made on this comment """
        return (
            sa.select(sa.func.count())
            .select_from(sa.select(CommentLike)
                         .join(Comment, isouter=True)
                         .where(CommentLike.comment_id == self.id)
                        )
        )
    #sa.select(sa.func.count()).select_from(CommentLike)
    
    @property
    def unlikes_count(self):
        """ count the number of unlikes made on this comment """
        return (
            sa.select(sa.func.count())
            .select_from(sa.select(CommentUnLike)
                         .join(Comment, isouter=True)
                         .where(CommentLike.comment_id == self.id)
                        )
        )