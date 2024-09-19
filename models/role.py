from models.image_upload import ImageUpload
from models.imports import *
from models.base_model import BaseModel, Base

user_role_association = Table(
    'user_role_association',
    Base.metadata,
    Column(
        'user_id', String(60), ForeignKey('users.id'), primary_key=True, nullable=False
    ),
    Column(
        'role_id', String(60), ForeignKey('roles.id'), primary_key=True, nullable=False
    )
)


class Role(BaseModel, Base):
    """ Represent a role

    """

    if os.getenv('STORAGE') in ['db', 'DB']:
        __tablename__ = 'roles'
        role = Column(String(80), nullable=False)
        users = relationship(
            'User',
            secondary=user_role_association,
            backref='roles',
            lazy=True
        )

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
