from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def verify_email(user_email, code):
    html_content = render_to_string(
        'mails/accounts_send_code.html',
        {
            'code': code,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Verification code',
        body=f"Your code is: {code}",
        from_email='winvat@yandex.ru',
        to=(user_email,),
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
