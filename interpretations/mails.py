from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.db.models.loading import get_model

def send_interpret_added(interpretation_id):
    Interpretation = get_model('interpretations', 'Interpretation')
    interpretation = Interpretation.objects.get(id = interpretation_id)

    target_user = interpretation.user
    composition_uploader = interpretation.composition.uploader
    composition_artist = interpretation.composition.artist

    to_user = []

    MailOptions = get_model('accounts', 'MailOptions')
    composition_uploader_options = MailOptions.objects.get(user=composition_uploader)
    composition_artist_options = MailOptions.objects.get(user=composition_artist)

    if (composition_uploader.is_active  and not (target_user.id == composition_uploader.id) and composition_uploader_options.interpret):
        to_user.append(composition_uploader.email)

    if (composition_artist.is_active  and not (target_user.id == composition_artist.id) and composition_artist_options.interpret):
        to_user.append(composition_artist.email)

    if not to_user:
        return 'send_interpret_added: Counld not find valid recepient for interpretation: {0}'.format(interpretation.id)

    to = to_user
    subject = target_user.name + " wrote a tale " + interpretation.title + " about " + interpretation.composition.title
    from_email = 'ThirdDime <notifications@thirddime.com>'

    ctx = {
        'target_name': target_user.name,
        'target_slug': target_user.slug,
        'target_picture': target_user.picture.url,
        'art_name': interpretation.composition.title,
        'art_slug': interpretation.composition.slug,
        'interpret_name': interpretation.title,
        'interpret_slug': interpretation.slug,
        'interpret_owner_slug': interpretation.user.slug,
    }

    message = get_template('mails/interpretations/added_tale.html').render(Context(ctx))
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


