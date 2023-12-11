from django.db import models


class UserManager(models.Manager):
    def get_or_none(self, **kwargs):
        result = self.get_queryset().filter(**kwargs)
        return result[0] if len(result) != 0 else None