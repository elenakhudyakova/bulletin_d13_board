from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, EmailVerificationCode
from .tasks import verify_email


@receiver(post_save, sender=EmailVerificationCode)
def send_email_verification_code(sender, instance, **kwargs):
    verify_email.delay(instance.user.email, instance.code)


@receiver(post_save, sender=User)
def create_verification_code(sender, instance, created, **kwargs):
    if not created or instance.email_verified:
        return

    if not EmailVerificationCode.objects.filter(user=instance).exists():
        code = EmailVerificationCode.objects.create(user=instance)
