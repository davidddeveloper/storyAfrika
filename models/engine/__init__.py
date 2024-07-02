from .file_storage import FileStorage
from .db_storage import DBStorage
import os

if os.getenv('STORAGE') in ['db', 'DB']:
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
