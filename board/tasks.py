from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Reply


@shared_task
def send_reply_to_email_task(reply_pk):
    reply = Reply.objects.select_related('author', 'ad', 'ad__author') \
        .defer('author__password', 'ad__content', 'ad__author__password').get(pk=reply_pk)
    html_content = render_to_string('mails/board_reply.html', {'reply': reply})
    msg = EmailMultiAlternatives(
        subject='На ваше объявление откликнулись',
        body=f"Пользователь {reply.author} ответил на ваше объявление:\n{reply.content}",
        from_email=settings.EMAIL_FROM,
        to=(reply.ad.author.email,),
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_email_when_reply_accepted_task(reply_pk):
    reply = Reply.objects.select_related('author', 'ad', 'ad__author') \
        .defer('author__password', 'ad__content', 'ad__author__password').get(pk=reply_pk)
    html_content = render_to_string('mails/board_reply_accept.html', {'reply': reply})
    msg = EmailMultiAlternatives(
        subject='Ваш отклик приняли',
        body=f"Пользователь {reply.ad.author} принял ваш отклик.",
        from_email=settings.EMAIL_FROM,
        to=(reply.author.email,),
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
