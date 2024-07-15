import os

if os.getenv('STORAGE') in ['db', 'DB']:
    from .db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from .file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
