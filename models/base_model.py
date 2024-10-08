#!/usr/bin/python3

"""
    base_model: represents shared attributes for all other class
                in the models folder

"""

import os
import uuid
import datetime
from models.imports import *

if os.getenv('STORAGE') in ['db', 'DB']:
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """ represents the blueprint for other clases

        Attributes:
            id - a string representing the uuid of the instance
            created_at - date and time the instance was created at
            updated_at - the date and time the instance was modify

    """

    if os.getenv('STORAGE') in ['db', 'DB']:
        id = Column(String(60), primary_key=True, default=str(uuid.uuid4()))
        created_at = Column(DateTime, default=datetime.datetime.now())
        updated_at = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, *args, **kwargs):

        if kwargs:
            for key, val in kwargs.items():
                if key != '__class__':
                    setattr(self, key, val)

            if 'id' in kwargs and isinstance(kwargs.get('id'), str):
                self.id = kwargs.get('id')
            else:
                self.id = str(uuid.uuid4())

            if 'created_at' in kwargs and isinstance(
                    kwargs.get('created_at'), str
                    ):
                self.created_at = datetime.datetime.fromisoformat(
                    kwargs.get('created_at')
                )
            else:
                self.created_at = datetime.datetime.now()

            if 'updated_at' in kwargs and isinstance(
                    kwargs.get('updated_at'), str
                    ):
                self.updated_at = datetime.datetime.fromisoformat(
                    kwargs.get('updated_at')
                )
            else:
                self.updated_at = datetime.datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary representation of the object """

        dictionary = self.__dict__.copy()
        try:
            dictionary['updated_at'] = dictionary['updated_at'].isoformat()
            dictionary['created_at'] = dictionary['created_at'].isoformat()
            dictionary['__class__'] = self.__class__.__name__
        except Exception:
            pass

        try:
            del dictionary['_sa_instance_state']
        except Exception:
            pass

        return dictionary
    
    def paginate(query, page, per_page):
        """ handles pagination

            - query: sqlalchemy query
            - page: a page number
            - per_page: number representing items per page

        """
        from models.engine import storage
    
        total_items = storage._session.query(func.count()).select_from(query.subquery()).scalar()
        total_pages = (total_items // per_page) + (1 if total_items % per_page > 0 else 0)
        # offset is very crucial as it specify the starting point of the query
        paginated_query = query.offset((page - 1) * per_page).limit(per_page)
        items = storage._session.execute(paginated_query).scalars().all()

        return {
            'total_items': total_items,
            'total_pages': total_pages,
            'page': page,
            'per_page': per_page,
            'items': items
        }

    def paginate_list(stories=[], page=1, per_page=4):
        """ Paginate an list

            - page: the current page
            - per_page: the number of items to get for that page

        """

        total_items = len(stories)
        total_pages = (total_items // per_page) + (1 if total_items % per_page > 0 else 0)
        paginated_result = [item for idx, item in enumerate(stories[((page - 1) * per_page):]) if idx < per_page]

        return {
            'total_items': total_items,
            'total_pages': total_pages,
            'page': page,
            'per_page': per_page,
            'items': paginated_result
        }

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}.{self.id}] {self.to_dict()}"

    def save(self):
        """ write the object to storage """
        from models.engine import storage

        storage.new(self)
        self.updated_at = datetime.datetime.now()
        storage.save()

    def delete(self):
        """ Deletes an object """
        from models.engine import storage

        storage.delete(self)
