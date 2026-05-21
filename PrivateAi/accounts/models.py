from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # email = models.EmailField(unique=True)
    email = models.EmailField(unique=False)
    used_storage = models.BigIntegerField(default=0)