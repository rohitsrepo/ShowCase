import os, django, shutil
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShowCase.settings")
django.setup()

import random
import string
from compositions.models import Composition
from interpretations.models import Interpretation
from feeds.models import StaffPost
from accounts.models import User
from django.core.files import File
from comments.models import Comment

def delete_existing_data():
    User.objects.all().delete()
    print "Deleted Users"
    Composition.objects.all().delete()
    print "Deleted compositions"
    Interpretation.objects.all().delete()
    print "Deleted interpretations"
    StaffPost.objects.all().delete()
    print "Deleted posts"
    shutil.rmtree('../media')
    print "Deleted media"

def add_composition_data(composition):
    image_num = random.randint(1, 5)
    image_path = "devScripts/resources/image{0}.jpg".format(image_num)
    composition.matter = (File(open(image_path)))
    composition.title = ['The Scream', 'Heat of Ice', "Tale of Brittle Truth", 'journey to end'][random.randint(0,3)]
    composition.artist = get_word() + ' ' + get_word()
    composition.save()

def get_word():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(2,5))

def add_interpretations(composition, uploader):
    for i in range(5):
        interpretation = Interpretation.objects.create(composition=composition, user=uploader, public=True)
        add_interpretation(interpretation)
        print "Interpretation"

def get_text(lower, upper):
    content = get_word()
    for i in range(lower, upper):
        content = content + ' ' + get_word()

    return content

def add_comments(interpretation, user):
    for i in range(random.randint(2,5)):
        Comment.objects.create(commenter=user, interpretation=interpretation, comment=get_text(25, 50))

def add_interpretation(interpretation):
    interpretation.interpretation = get_text(100, 200)
    interpretation.save()
    add_comments(interpretation, interpretation.user)

delete_existing_data()
for i in range(1, 10):
    print "Creating objects"
    uploader = User.objects.create_user("user" + str(i) + "@user.com", "user" + str(i), "user")
    print "uploader"
    print uploader.first_name
    composition = Composition(uploader=uploader)
    add_composition_data(composition)
    print "Composition"
    print composition.title
    add_interpretations(composition, uploader)
    print "Added interpretations to composition"
    post = StaffPost.objects.create(composition=composition, interpretation=composition.interpretation_set.all()[random.randint(0, 4)])
    print "Post"