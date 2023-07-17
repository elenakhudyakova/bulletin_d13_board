from django.contrib import admin

from .models import User, EmailVerificationCode

admin.site.register(User)
admin.site.register(EmailVerificationCode)
