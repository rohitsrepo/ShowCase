from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.db.models.loading import get_model

def send_warm_welcome(user_id):
    User = get_model('accounts', 'User')
    user = User.objects.get(id=user_id)

    subject = 'Welcome to ThirdDime'
    to = [user.email]
    from_email = 'Rohit Kumar <rohit@thirddime.com>'
    message = render_to_string('mails/accounts/warm_welcome.txt')

    count = 1
    while count:
        try:
            EmailMessage(subject, message, to=to, from_email=from_email).send(fail_silently=False)
            break;
        except:
            if (count > 3):
                raise
            count += count

def send_welcome(user_id):
    User = get_model('accounts', 'User')
    user = User.objects.get(id=user_id)

    subject = "Welcome to ThirdDime"
    to = [user.email]
    from_email = 'ThirdDime Team <info@thirddime.com>'

    ctx = {
        'username': user.name,
    }

    message = get_template('mails/accounts/welcome.html').render(Context(ctx))
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