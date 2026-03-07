from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Our Site!"
        message = f"Hi {instance.username},\n\nThank you for registering with us!"
        from_email = settings.EMAIL_HOST_USER if hasattr(settings, "EMAIL_HOST_USER") else "noreply@example.com"
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)