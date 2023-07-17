from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Reply
from .tasks import send_reply_to_email_task, send_email_when_reply_accepted_task


@receiver(post_save, sender=Reply)
def send_reply_to_email_signal(sender, instance, created, **kwargs):
    if created:
        send_reply_to_email_task.delay(instance.pk)


@receiver(post_save, sender=Reply)
def send_email_when_reply_accepted_signal(sender, instance, update_fields, **kwargs):
    if instance.is_accepted and update_fields is not None and 'is_accepted' in update_fields:
        send_email_when_reply_accepted_task.delay(instance.pk)
