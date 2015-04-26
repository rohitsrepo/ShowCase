import os, django, shutil
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShowCase.settings")
django.setup()

from compositions.models import Composition
from compositions.imageTools import generate_size_versions

def main():
	compositions = Composition.objects.all()
	for composition in compositions:
		image_path = composition.matter.path
		print "Resizing"
		print image_path
		generate_size_versions(image_path)

main();
