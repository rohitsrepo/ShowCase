import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShowCase.settings")
django.setup()

import random
import string
from compositions.models import Composition
from interpretations.models import Interpretation
from feeds.models import StaffPost
from accounts.models import User
from django.core.files import File

def delete_existing_data():
	User.objects.all().delete()
	print "Deleted Users"
	Composition.objects.all().delete()
	print "Deleted compositions"
	Interpretation.objects.all().delete()
	print "Deleted interpretations"
	StaffPost.objects.all().delete()
	print "Deleted posts"

def add_composition_data(composition):
	image_num = random.randint(1, 5)
	image_path = "devScripts/resources/image{0}.jpg".format(image_num)
	composition.matter = (File(open(image_path)))
	composition.title = ['The Scream', 'Heat of Ice', "Tale of Brittle Truth", 'journey to end'][random.randint(0,3)]
	composition.save()

def get_word():
	return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(2,5))

def add_interpretations(composition, artist):
	for i in range(5):
		interpretation = Interpretation.objects.create(composition=composition, user=artist)
		print add_interpretation(interpretation)
		print "Interpretation"

def add_interpretation(interpretation):
	content = get_word()
	for i in range(100, 200):
		content = content + ' ' + get_word()
	interpretation.interpretation = content
	interpretation.save()

delete_existing_data()
for i in range(1, 10):
	print "Creating objects"
	artist = User.objects.create_user("user" + str(i) + "@user.com", "user" + str(i), "user")
	print "Artist"
	print artist.first_name
	composition = Composition.objects.create(artist=artist)
	add_composition_data(composition)
	print "Composition"
	print composition.title
	add_interpretations(composition, artist)
	print "Added interpretations to composition"
	post = StaffPost.objects.create(composition=composition, interpretation=composition.interpretation_set.all()[random.randint(0, 4)])
	print "Post"