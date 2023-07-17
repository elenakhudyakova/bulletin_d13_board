import secrets
import string
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from .manager import UserManager


def generate_code():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(6))


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    email_verified = models.BooleanField(default=False)

    objects = UserManager()


class EmailVerificationCode(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=generate_code)
    datetime_update = models.DateTimeField(auto_now=True)

    def generate_new_code(self):
        self.code = generate_code()
        self.save()

    def check_time(self):
        return now() - self.datetime_update > datetime.timedelta(minutes=5)
