"""
    user: represent a model for creating users

"""

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import WriteOnlyMapped

from models.imports import *
from models.base_model import Base, BaseModel
from models.story import Story
from models.image_upload import ImageUpload
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, ImageUpload, Base):
    """
        Represents a user

        Attributes:
            - username: user identity on the platform
            - fullname: first name last name and any other name
            - email: user email address
            - password: password of the user
            - short_bio: who the user is
            - about: detail description of the user
    """
    from models.follower import Follower

    if os.getenv('STORAGE') in ['db', 'DB']:
        __tablename__ = 'users'
        username = Column(String(80), nullable=False)
        email = Column(String(120), nullable=False)
        password = Column(String(200), nullable=False)
        short_bio = Column(String(160), nullable=True)
        about = Column(Text, nullable=True)
        first_name = Column(String(50), nullable=True)
        last_name = Column(String(50), nullable=True)
        full_name = Column(String(50), nullable=True, default=(first_name + ' ' + last_name))
        stories = relationship('Story', backref='writer', lazy=True)
        comments = relationship('Comment', backref='commenter', lazy=True)
        likes = relationship('Like', backref='liker', lazy=True)
        bookmarks = relationship('Bookmark', backref='bookmarker', lazy=True)
        comment_likes = relationship('CommentLike', backref='liker', lazy=True)
        comment_unlikes = relationship('CommentUnLike', backref='unliker', lazy=True)
        followers:  WriteOnlyMapped['User'] = relationship(
            secondary=Follower.__table__,
            primaryjoin='followers.c.followed_id == User.id',
            secondaryjoin='followers.c.follower_id == User.id',
            back_populates='following',
            lazy=True
        )
        following: WriteOnlyMapped['User'] = relationship(
            secondary=Follower.__table__,
            primaryjoin='followers.c.follower_id == User.id',
            secondaryjoin='followers.c.followed_id == User.id',
            back_populates='followers',
            lazy=True
        )
        topic_following = relationship(
            'TopicFollower',
            backref='users',
            lazy=True
        )
        avatar = Column(String(100), nullable=True) # path to avatar

    else:
        _username = ''
        _email = ''
        _password = ''
        _short_bio = ''
        _about = ''

    def __init__(
            self, username, email, password, **kwargs
            ):
        super().__init__(**kwargs)

        arguments = {
            'username': username,
            'email': email,
            'password': password
        }
        for argument, value in arguments.items():
            if not isinstance(value, str):
                raise ValueError(f"{argument} must ba a string")

            setattr(self, argument, value)

    def to_dict(self):
        """ Dictionary representation of the object """

        dictionary = super().to_dict()
        try:
            dictionary.pop('password')
            dictionary.pop('_sa_instance_state')
        except Exception:
            pass

        return dictionary

    def set_password(self, password):
        """ saves the password as hash """
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """ map a given password against a password hash """
        return check_password_hash(self.password, password)

    def liked_story(self, story_id):
        from models.engine import storage
        from models.like import Like

        story_likes = sa.select(Story).join(Like).where(sa.and_(
            Story.id == story_id,
            User.id == self.id
        ))

        if storage._session.query(story_likes.subquery()).all() != []:
            return True
        else:
            return False
    
    def liked_comment(self, comment_id):
        """ check if a comment is liked """
        pass

    def follow(self, user):
         """
            follow a user

            - user: a user instance
         """

         if not self.is_following(user):
             self.following.add(user)

    def unfollow(self, user):
        """
            unfollow a user

            - user: a user instance
         """

        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        """ checks if a user is following another user

            - user: a user

            Return: true if self is following user
        """
        from models.engine import storage

        query = self.following.select().where(User.id == user.id)
        return storage._session.scalar(query) is not None

    @property
    def followers_count(self):
        """ count the number of followers self has """
        from models.engine import storage

        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return storage._session.scalar(query)

    @property
    def following_count(self):
        """ count the number of people self is following """
        from models.engine import storage

        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())

        return storage._session.scalar(query)

    @property
    def following_stories(self):
        """ gets the stories from all the users self is following
            and own stories

        """

        from models.engine import storage
        Writer = so.aliased(User)
        Follower = so.aliased(User)

        # join story with writer of the story and followers of that writer
        return (
            sa.select(Story)
            .join(Story.writer.of_type(Writer))
            .join(Writer.followers.of_type(Follower), isouter=True)
            .where(sa.or_(
                Follower.id == self.id,
                Writer.id == self.id
            ))
            .group_by(Story)
            .order_by(Story.created_at.desc())
        )

    @property
    def get_comments(self):
        """ gets all the comments for that specific user """
        pass

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError(
                "No `id` attribute - override `get_id`"
            ) from None
