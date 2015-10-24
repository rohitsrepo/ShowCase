from django.template.loader import render_to_string
from django.core.mail import EmailMessage

def send_warm_welcome(user):
    subject = 'Welcome to ThirdDime'
    to = [user.email]
    from_email = 'Rohit Kumar <rohit@thirddime.com>'
    message = render_to_string('mails/accounts/warm_welcome.txt')

    EmailMessage(subject, message, to=to, from_email=from_email).send(fail_silently=False)