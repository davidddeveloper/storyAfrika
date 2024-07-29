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
        story_id = Column('Story', ForeignKey('stories.id'), nullable=False)
        user_id = Column('User', ForeignKey('users.id'), nullable=False)
        likes = relationship('CommentLike', backref='comment', lazy=True)
        unlikes = relationship('CommentUnLike', backref='comment', lazy=True)

    else:
        comment = ''
        story_id = ''
        user_id = ''

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
        comment_like = CommentLike(comment_id=self.id, user_id=user_id)

        if self.is_liked_by(user_id):  # user already liked the story
            return True
        
        if not self.is_liked_by(user_id) and not self.is_unliked_by(user_id):
            # not liked or unliked the story yet
            comment_like.save()

        elif self.is_unliked_by(user_id):  # used to unliked the comment
            # get the unlike
            comment_unlike = storage._session.query(CommentUnLike).where(sa.and_(
                CommentUnLike.user_id == user_id,  # get only the comments that the user has liked
                CommentUnLike.comment_id == self.id
            ))
            comment_unlike.delete()
            # create the new like
            comment_like.save()
            storage.save()

        storage.close()
        return 'success'

    def unlike(self, user_id):
        """ like a comment 
        
            Attribute:
                - user_id: the id of the user that wants to like a comment

        """
        from models.engine import storage

        comment_unlike = CommentUnLike(comment_id=self.id, user_id=user_id)

        if self.is_unliked_by(user_id):  # user is has already unliked the story
            return True

        if not self.is_liked_by(user_id) and not self.is_unliked_by(user_id):
            comment_unlike.save()
        elif self.is_liked_by(user_id):
            comment_like = storage._session.query(CommentLike).where(sa.and_(
                CommentLike.user_id == user_id,  # get only the comments that the user has liked
                CommentLike.comment_id == self.id
            ))
            comment_like.delete()
            comment_like.save()

            comment_unlike.save()
            storage.save()

        storage.close()
        return 'success'
    
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
        storage.close()
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
        storage.close()
        return result is not None
        
    @property
    def likes_count(self):
        """ count the number of likes made on this comment """
        return len(self.likes)
    
    @property
    def unlikes_count(self):
        """ count the number of unlikes made on this comment """
        return len(self.unlikes)