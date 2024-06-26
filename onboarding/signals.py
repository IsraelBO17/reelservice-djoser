from django.dispatch import Signal, receiver
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from .utils import encode_uid

# Send invitation mail.
send_invite_mail = Signal()

# Deactivate Employee User
deactivate_employee_user = Signal()

@receiver(send_invite_mail)
def send_invitation_mail(sender, user, request, **kwargs):
    uid = encode_uid(user.pk)
    token = default_token_generator.make_token(user)
    context = {
        'site_name': settings.SITE_NAME,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': settings.DOMAIN,
        'url': f'employee-invitation/{uid}/{token}',
    }
    sender = settings.AWS_SES_FROM_EMAIL

    response = user.send_mail(email_template='invite', sender=sender, context=context)
    return response

@receiver(deactivate_employee_user)
def deactivate_employee_user(sender, user, **kwargs):
    user.is_active = False
    user.save()


