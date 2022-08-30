from django.db import models


class BaseModel(models.Model):
    """
    Base model to store created and updated at timestamps of the records.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
