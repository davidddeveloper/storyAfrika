"""
    user: represent a model for creating users

"""

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import WriteOnlyMapped

from models.imports import *
from models.base_model import Base, BaseModel
from models.story import Story
from models.bookmark import Bookmark
from models.like import Like
from models.role import Role
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
        stories = relationship('Story', backref='writer', lazy=True, passive_deletes=True, cascade='all, delete-orphan')
        #my_topics = relationship('Topic', backref='creator', lazy=True, passive_deletes=True, cascade='all, delete-orphan')
        comments = relationship('Comment', backref='commenter', lazy=True, passive_deletes=True, cascade='all, delete-orphan')
        likes = relationship('Like', backref='liker', lazy=True, passive_deletes=True, cascade='all, delete-orphan')
        bookmarks = relationship('Bookmark', backref='bookmarker', lazy=True, passive_deletes=True, cascade='all, delete-orphan')
        comment_likes = relationship('CommentLike', backref='liker', lazy=True, passive_deletes=True, cascade='all, delete-orphan')
        comment_unlikes = relationship('CommentUnLike', backref='unliker', lazy=True, passive_deletes=True, cascade='all, delete-orphan')
        followers:  WriteOnlyMapped['User'] = relationship(
            secondary=Follower.__table__,
            primaryjoin='followers.c.followed_id == User.id',
            secondaryjoin='followers.c.follower_id == User.id',
            back_populates='following',
            passive_deletes=True,
            lazy=True
        )
        following: WriteOnlyMapped['User'] = relationship(
            secondary=Follower.__table__,
            primaryjoin='followers.c.follower_id == User.id',
            secondaryjoin='followers.c.followed_id == User.id',
            back_populates='followers',
            passive_deletes=True,
            lazy=True
        )
        topic_following = relationship(
            'TopicFollower',
            backref='user', # I should remember to change users to user here and in my templates
            lazy=True
        )
        avatar = Column(String(200), nullable=True) # path to avatar
        banner = Column(String(200), nullable=True, default='https://fastly.picsum.photos/id/91/800/500.jpg?hmac=J_kCOn2MZlDuJIb_rU14DYnb6HMv55ynWirbSF9l8f0')

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
        except KeyError:
            pass
        try:
            dictionary.pop('_sa_instance_state')
        except KeyError:
            pass


        dictionary.pop('stories', None)
        dictionary.pop('likes', None)
        dictionary.pop('bookmarks', None)
        dictionary.pop('comments', None)
        
        dictionary['roles'] = [role.to_dict() for role in self.roles]
        

        return dictionary

    def set_password(self, password):
        """ saves the password as hash """
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """ map a given password against a password hash """
        return check_password_hash(self.password, password)

    def liked_story(self, story_id):
        """ check if the user has liked the story """
        from models.engine import storage
        from models.like import Like

        story_like = sa.select(Like).where(sa.and_(
            Like.story_id == story_id,
            Like.user_id == self.id
        ))

        result = storage._session.execute(story_like).scalar_one_or_none()
        return result is not None
    
    def bookmarked_story(self, story_id):
        """ check if a user has bookmarked the story """
        from models.engine import storage
        from models.bookmark import Bookmark

        story_bookmark = sa.select(Bookmark).where(sa.and_(
            Bookmark.story_id == story_id,
            Bookmark.user_id == self.id
        ))

        result = storage._session.execute(story_bookmark).scalar_one_or_none()
        return result is not None
    
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

    def set_default_profile(self, path=None):
        if path is None:
            self.avatar = f'https://api.dicebear.com/9.x/initials/svg?seed={self.username}'
        else:
            self.avatar = path
        self.save()

        return self.avatar

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
    def stories_written_count(self):
        """ count the number of people self is following """
        from models.engine import storage

        query = sa.select(sa.func.count()).select_from(
            sa.select(Story).where(Story.user_id == self.id))

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
    def foryou_stories(self):
        """Gets the stories that the user has not liked or bookmarked."""
        from models.engine import storage
        import sqlalchemy as sa

        # Subquery to check if the story is liked or bookmarked by the user
        liked_subquery = (
            sa.select(Like.story_id)
            .where(Like.user_id == self.id)
            .subquery()
        )

        bookmarked_subquery = (
            sa.select(Bookmark.story_id)
            .where(Bookmark.user_id == self.id)
            .subquery()
        )

        # Main query for stories not liked or bookmarked by the user
        return (
            sa.select(Story)
            .join(User, Story.user_id == User.id)
            .outerjoin(liked_subquery, liked_subquery.c.story_id == Story.id)
            .outerjoin(bookmarked_subquery, bookmarked_subquery.c.story_id == Story.id)
            .where(Story.user_id != self.id)  # Stories from other users
            .where(liked_subquery.c.story_id == None)  # Exclude liked stories
            .where(bookmarked_subquery.c.story_id == None)  # Exclude bookmarked stories
            .group_by(Story.id)
            .order_by(Story.created_at.desc())
        )


    @property
    def stories_bookmarked(self):
        """ get all the stories bookmarked by the user """
        from models.engine import storage
    
        return (
            storage._session.query(Story).join(Bookmark).where(sa.and_(
                Bookmark.user_id == self.id,
                Bookmark.story_id == Story.id
            )).order_by(Story.created_at.asc())
        )

    def search_stories_bookmarked(self, data):
        """ """
        return (
            self.stories_bookmarked
            .where(Story.title.contains(data))
            .order_by(Bookmark.created_at.asc())
        )


    @classmethod
    def search_by_username(cls, data):
        """ retrive users base on their username """
        from models.engine import storage
        return storage._session.query(cls).where(cls.username.contains(data))

    def search_users(self, data):
        from models.engine import storage
        storage.query(User)
        pass

    @property
    def following_topics(self):
        """ All the topics a user is following """
        pass

    @property
    def stories_from_topic(self, topic):
        """ All stories from a specific topic a user is following """
        pass

    @property
    def stories_from_topics(self):
        """ All stories from all the topics a user is following """
        pass

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
