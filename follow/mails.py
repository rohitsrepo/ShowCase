from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage

from accounts.models import User

def send_follow(user_id, action_user_id):
    user = User.objects.get(id=user_id)
    action_user = User.objects.get(id=action_user_id)

    subject = action_user.name + " is now following you"
    to = [user.email]
    from_email = 'ThirdDime <info@thirddime.com>'

    ctx = {
        'target_name': action_user.name,
        'target_slug': action_user.slug,
        'target_picture': action_user.picture.url,
    }

    message = get_template('mails/follow/follow.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'

    while count:
        try:
            msg.send(fail_silently=False)
            break;
        except:
            if (count > 3):
                raise
            count += count