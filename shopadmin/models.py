from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_shop_owner = models.BooleanField(default=False)
    is_storekeeper = models.BooleanField(default=False)
