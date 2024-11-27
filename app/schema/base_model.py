import django.contrib
from django.db import models
from uuid import uuid4
from datetime import datetime
import django

class Base(models.Model):
    """ represents the blueprint for other clases

        Attributes:
            id - a string representing the uuid of the instance
            created_at - date and time the instance was created at
            updated_at - the date and time the instance was modify

    """

    id = models.UUIDField(primary_key=True, default=uuid4, null=False)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    class Meta:
        abstract = True

    # pagination