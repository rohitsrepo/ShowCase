import requests

from allaccess.models import AccountAccess
from accounts.userfollows import follow_bulk, add_followers_bulk
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

def get_friends_twitter(tracker):
    return get_contacts_twitter(tracker, 'https://api.twitter.com/1.1/friends/ids.json')

def get_followers_twitter(tracker):
    return get_contacts_twitter(tracker, 'https://api.twitter.com/1.1/followers/ids.json')

def get_contacts_twitter(tracker, url):
    from allaccess.clients import get_client
    client = get_client(tracker.access.provider)

    try:
        response = client.request('get', url, token=tracker.access.access_token)
        return response.json()
    except e:
        tracker.remarks = 'Failed to get twitter friends: {0}'.format(e)
        tracker.save()
        return None


def get_social_contact(tracker):
    if tracker.access.provider.name == 'facebook':
        contacts = get_social_contact_fb(tracker)
        print contacts
        contact_ids = [contact['id'] for contact in contacts]
        return (contact_ids, contact_ids)
    elif tracker.access.provider.name == 'google':
        contacts = get_social_contact_google(tracker)
        contact_ids = [contact['id'] for contact in contacts]
        return (contact_ids, contact_ids)
    elif tracker.access.provider.name == 'twitter':
        friends = get_friends_twitter(tracker)['ids']
        followers = get_followers_twitter(tracker)['ids']
        return (friends, followers)
    else:
        return "NATIVE"

def update_follows_by_social():
    populate_tracker()
    trackers = get_non_processed_accounts()

    for tracker in trackers:
        return get_social_contact(tracker)

def update_follow_from_social(access_id):
    access = AccountAccess.objects.get(id=access_id)
    user = access.user
    tracker, created = SocialTracker.objects.get_or_create(access=access)

    if not tracker.status:
        (to_follow, followers) = get_social_contact(tracker)

        print "Got the CROWD"
        print (to_follow, followers)

        to_follow_users = []
        for target in to_follow:
            try:
                target_user = AccountAccess.objects.get(identifier = target).user
                print "follow: " + target_user.name
                to_follow_users.append(target_user)
            except AccountAccess.DoesNotExist:
                pass

        following_users = []
        for target in followers:
            try:
                target_user = AccountAccess.objects.get(
                    identifier=target,
                    provider=access.provider).user
                following_users.append(target_user)
            except AccountAccess.DoesNotExist:
                pass

        follow_bulk(user, to_follow_users)
        add_followers_bulk(following_users, user)

        remarks = 'to_follow_found:to_follow_added {0}:{1} and followers_found:followers_added {2}:{3}'.format(
            len(to_follow),
            len(to_follow_users),
            len(followers),
            len(following_users))

        print remarks

        # tracker.status = True
        # tracker.save()