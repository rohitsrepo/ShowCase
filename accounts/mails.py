from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

def send_warm_welcome(user):
    subject = 'Welcome to ThirdDime'
    to = [user.email]
    from_email = 'Rohit Kumar <rohit@thirddime.com>'
    message = render_to_string('mails/accounts/warm_welcome.txt')

    EmailMessage(subject, message, to=to, from_email=from_email).send(fail_silently=False)

def send_welcome(user):
    subject = "Welcome to ThirdDime"
    to = [user.email]
    from_email = 'ThirdDime Team <info@thirddime.com>'

    ctx = {
        'username': user.name,
    }

    message = get_template('mails/accounts/welcome.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send(fail_silently=False)