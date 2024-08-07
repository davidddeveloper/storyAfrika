"""
    user: represent a model for creating users

"""

from models.imports import *
from models.base_model import Base, BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, Base):
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

    if os.getenv('storage') in ['db', 'DB']:
        __tablename__ = 'users'
        username = Column(String(80), nullable=False)
        email = Column(String(120), nullable=False)
        password = Column(String(200), nullable=False)
        short_bio = Column(String(160), nullable=True)
        about = Column(Text, nullable=True)
        stories = relationship('Story', backref='writer', lazy=True)
        comments = relationship('Comment', backref='commenter', lazy=True)
        likes = relationship('Like', backref='liker', lazy=True)
        bookmarks = relationship('Bookmark', backref='bookmarker', lazy=True)
        followers = relationship(
            'Follower',
            foreign_keys='Follower.followed_id',
            backref='followed',
            lazy=True
        )
        following = relationship(
            'Follower',
            foreign_keys='Follower.follower_id',
            backref='follower',
            lazy=True
        )
        topic_following = relationship(
            'TopicFollower',
            backref='users',
            lazy=True
        )

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

    def set_password(self, password):
        """ saves the password as hash """
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """ map a given password against a password hash """
        return check_password_hash(self.password, password)

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
