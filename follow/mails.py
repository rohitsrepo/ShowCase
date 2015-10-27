from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.db.models.loading import get_model

def send_follow(user_id, action_user_id):
    if user_id == action_user_id:
        return "send_follow: Action user is same as the target user"

    User = get_model('accounts', 'User')
    user = User.objects.get(id=user_id)
    MailOptions = get_model('accounts', 'MailOptions')
    mail_options = MailOptions.objects.get(user=user)
    if not mail_options.follow:
        return "User disabeled follow mails"
    
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

    count = 1
    while count:
        try:
            msg.send(fail_silently=False)
            break;
        except:
            if (count > 3):
                raise
            count += count