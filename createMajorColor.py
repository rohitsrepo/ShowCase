import os, django, shutil
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShowCase.settings")
django.setup()

import requests

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

def validate_friends_permission_fb(tracker, url, access_token):
        try:
            response = requests.get(url, params=access_token)

            if response.ok:
                try:
                    response = response.json()
                    if ('summary' in response.keys()):
                        total_friends = response['summary']['total_count']
                        tracker.remarks = "Total friends: {0}".format(total_friends)
                        tracker.save()
                        return True

                except requests.exceptions.ReadTimeout:
                    tracker.remarks = "Request timed out for validating friends permission: {0}".format(response.url)
                    tracker.save()
                    return False
                except ValueError:
                    tracker.remarks = "Unable to convert response to Json for validating friends permission: {0}".format(response.url)
                    tracker.save()
                    return False

        except requests.exceptions.ConnectionError:
            tracker.remarks = "Could not reach friends url while validating friends url: {0}".format(response.url)
            tracker.save()
            return False

        return False

def get_social_page_fb(tracker, url, access_token = ''):
        try:
            if access_token:
                response = requests.get(url, params=access_token)
            else:
                response = requests.get(url)

            if response.ok:
                try:
                    response = response.json()

                    if response['data']:
                        friends = response['data']
                    else:
                        return []

                    if response['paging']['next']:
                        friends.extend(get_social_page_fb(tracker, response['paging']['next']))

                    return friends

                except requests.exceptions.ReadTimeout:
                    tracker.remarks += "Request timed out: {0}".format(response.url)
                    tracker.save()
                    raise
                except ValueError:
                    tracker.remarks += "Unable to convert response to Json: {0}".format(response.url)
                    tracker.save()
                    raise

        except requests.exceptions.ConnectionError:
            tracker.remarks += "Could not reach friends url: {0}".format(response.url)
            tracker.save()
            raise

def get_social_contact_fb(tracker):
    access = tracker.access
    friends_url = "https://graph.facebook.com/v2.5/{}/friends".format(access.identifier)

    try:
        permissions = validate_friends_permission_fb(tracker, friends_url, access.access_token)
        if permissions:
            friends = get_social_page_fb(tracker, friends_url, access.access_token)
            return friends
        else:
            tracker.remarks = "Do not have friends permission"
            tracker.save()
    except:
        tracker.remarks += "Failed to get friends for access {0}, provider {1} and user {2}".format(access.id, access.provider.name, access.user.name)
        tracker.save()

def get_social_page_google(tracker, url, access_token = ''):
        try:
            if access_token:
                import ast
                response = requests.get(url, params=ast.literal_eval(access_token))
            else:
                response = requests.get(url)

            print response

            if response.ok:
                try:
                    response = response.json()

                    if 'kind' in response.keys():
                        friends = response['items']
                    else:
                        return []

                    return friends

                except requests.exceptions.ReadTimeout:
                    tracker.remarks += "Request timed out: {0}".format(response.url)
                    tracker.save()
                    raise
                except ValueError:
                    tracker.remarks += "Unable to convert response to Json: {0}".format(response.url)
                    tracker.save()
                    raise

        except requests.exceptions.ConnectionError:
            tracker.remarks += "Could not reach friends url: {0}".format(response.url)
            tracker.save()
            raise

def get_social_contact_google(tracker):
    access = tracker.access
    friends_url = "https://www.googleapis.com/plus/v1/people/{0}/people/visible".format(access.identifier)

    try:
        friends = get_social_page_google(tracker, friends_url, access.access_token)
        return friends
    except:
        tracker.remarks += "Failed to get friends for access {0}, provider {1} and user {2}".format(access.id, access.provider.name, access.user.name)
        tracker.save()

def get_social_contact(tracker):
    if tracker.access.provider.name == 'facebook':
        return get_social_contact_fb(tracker)
    elif tracker.access.provider.name == 'google':
        return get_social_contact_google(tracker)
    else:
        return "NATIVE"

def update_follows_by_social():
    populate_tracker()
    trackers = get_non_processed_accounts()

    for tracker in trackers:
        return get_social_contact(tracker)