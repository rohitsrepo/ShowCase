import os, django, shutil
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShowCase.settings")
django.setup()

import uuid
from accounts.models import User
from compositions.models import Composition

compositions = Composition.objects.all()

for composition in compositions:
	holder = str(uuid.uuid1())
	artist = composition.artist
	User.objects.create_user(
			holder+'@user.com',
			artist,
			holder,
			is_active = False,
			is_artist = True
		)