import os, django, shutil
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShowCase.settings")
django.setup()

from compositions.models import Composition
from compositions.colorTools import colorz

for composition in Composition.objects.all():
    print composition.slug
    try:
        major = colorz(composition.matter.path)
        print major[0]
        composition.major = major[0]
        composition.save()
    except:
        print "FAILED"