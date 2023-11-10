from datetime import timedelta

from django.core.mail import send_mail
from config import settings
from .models import Subscription
from celery import shared_task
from django.contrib.auth.models import User
from django.utils.timezone import now


@shared_task
def send_update_email(course_id):
    subscriptions = Subscription.objects.filter(course__id=course_id)
    emails = subscriptions.values_list('user__email', flat=True)

    send_mail(
        subject='Обновление курса',
        message='Материалы курса были обновлены.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False,
    )


@shared_task
def deactivate_inactive_users():
    month_ago = now() - timedelta(days=30)
    User.objects.filter(last_login__lt=month_ago).update(is_active=False)
