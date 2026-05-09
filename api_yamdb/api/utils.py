from django.core.mail import send_mail
from django.conf import settings


def send_confurm_mail(confirm_code, email):
    send_mail(
        subject='Ваш верификационный код',
        message=f'Ваш код: {confirm_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=(email,),
        fail_silently=False,)
