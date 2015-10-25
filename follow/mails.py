from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage


def send_follow(user, target_user):
    subject = target_user.name + " is now following you"
    to = [user.email]
    from_email = 'ThirdDime <info@thirddime.com>'

    ctx = {
        'target_name': target_user.name,
        'target_slug': target_user.slug,
        'target_picture': target_user.picture,
    }

    message = get_template('mails/follow/follow.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send(fail_silently=False)