import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShowCase.settings")
django.setup()

from compositions.models import Composition
from interpretations.models import Interpretation
from feeds.models import StaffPost
from accounts.models import User

for i in range(5, 15):
	print "Creating objects"
	artist = User.objects.create_user("poochi" + str(i) + "@user.com", "poochi" + str(i), "poochi")
	composition = Composition.objects.create(artist=artist)
	interpretation = Interpretation.objects.create(composition=composition, user=artist)
	post = StaffPost.objects.create(composition=composition, interpretation=interpretation)