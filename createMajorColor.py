import os, django, shutil
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShowCase.settings")
django.setup()

from allaccess.models import AccountAccess
from follow.models import SocialTracker


def populate_tracker():
	# Raw sql query would be better for Server scenarios
	new_access = AccountAccess.objects.filter(social_tracker=None)
	for access in new_access:
		SocialTracker.objects.create(access=access)

def get_non_processed_accounts():
	return SocialTracker.objects.filter(status=False)

def get_friends_url(access):
	if access.provider.name == 'facebook':
		return "https://graph.facebook.com/v2.5/{}/friends".format(access.identifier)
	else:
		return None

def get_social_contact(access):
	friends_url = get_friends_url(access)
	if friends_url:
		response = requests.get(friends_url, token=access.access_token)
		if response.ok:
			try:
				response = response.json()
				friends = response['data']  # Seriealize
				while response['paging']['next']:
					
