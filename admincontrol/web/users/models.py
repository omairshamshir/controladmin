from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AeeUser(AbstractBaseUser):
    first_name = models.CharField(max_length=12, blank=False)
    last_name = models.CharField(max_length=12, blank=False)
    username = models.CharField(max_length=12, blank=False, unique=True)
    email = models.EmailField(max_length=50, blank=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name
