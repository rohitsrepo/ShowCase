from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.db.models.loading import get_model

def send_admired(admiration_id):
    Admiration = get_model('admirations', 'Admiration')
    admiration = Admiration.objects.get(id=admiration_id)

    if admiration.admire_type == Admiration.ART:
        send_admired_composition(admiration)
    elif admiration.admire_type == Admiration.BUCKET:
        send_admired_bucket(admiration)
    else:
        raise Exception('send_admired_mail: Invalid admiration type found. Admiration:{0} with type: {1}'
            .format(admiration.id, admiration.admire_type))

def send_admired_composition(admiration):
    target_user = admiration.owner
    composition = admiration.content_object

    to_user = []

    composition_owner = composition.uploader
    if (composition_owner.is_active):
        to_user.append(composition_owner.email)

    composition_artist = composition.artist
    if composition_artist.is_active and not(composition_owner == composition_artist):
        to_user.append(composition_artist.email)

    if not to_user:
        raise Exception('send_admired_composition: Counld not find valid recepient for admiration: {0}'.format(admiration.id))

    to = to_user
    subject = target_user.name + " admired artwork " + composition.title
    from_email = 'ThirdDime <info@thirddime.com>'

    ctx = {
        'target_name': target_user.name,
        'target_slug': target_user.slug,
        'target_picture': target_user.picture.url,
        'art_name': composition.title,
        'art_slug': composition.slug,
    }

    message = get_template('mails/admiration/admired_artwork.html').render(Context(ctx))
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


def send_admired_bucket(admiration):
    target_user = admiration.owner
    series = admiration.content_object

    subject = target_user.name + " admired series " + series.name
    to = [series.owner.email]
    from_email = 'ThirdDime <info@thirddime.com>'

    ctx = {
        'target_name': target_user.name,
        'target_slug': target_user.slug,
        'target_picture': target_user.picture.url,
        'series_name': series.name,
        'series_slug': series.slug,
        'series_owner_slug': series.owner.slug,
        'admire_as': admiration.admire_as.word,
    }

    message = get_template('mails/admiration/admired_series.html').render(Context(ctx))
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
