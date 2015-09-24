from django.http import HttpResponse
from allaccess.views import OAuthRedirect, OAuthCallback
from .models import User
from django.core.urlresolvers import reverse
from django.core.files import File
import urllib

class EmailPermissionRedirect(OAuthRedirect):

    def get_additional_parameters(self, provider):
        if provider.name == 'facebook':
            # Request permission to see user's email
            return {'scope': 'email'}
        if provider.name == 'google':
            # Request permission to see user's profile and email
            perms = ['userinfo.email', 'userinfo.profile']
            scope = ' '.join(['https://www.googleapis.com/auth/' + p for p in perms])
            return {'scope': scope}
        return super(EmailPermissionRedirect, self).get_additional_parameters(provider)

    def get_callback_url(self, provider):
        "Return the callback url for this provider."
        return reverse('auth-callback', kwargs={'provider': provider.name})


class CustomUserCallback(OAuthCallback):

    def get_login_type(self, provider):
        choice = [c[0] for c in User.LOGIN_CHOICES if c[1] == provider.name]
        return choice[0]

    def try_adding_picture(self, info, user, provider):
        picture_url = info.get('picture', None)

        if (picture_url != None):
            try:
                content = urllib.urlretrieve(picture_url)
                user.picture = File(open(content[0]))
                user.save()
                return;
            except Exception, e:
                pass

        if provider.name == 'facebook':
            try:
                picture_url = 'http://graph.facebook.com/' + info.get('id') + '/picture?type=large'
                content = urllib.urlretrieve(picture_url)
                user.picture = File(open(content[0]))
                user.save()
                return;
            except Exception, e:
                pass

    def get_or_create_user(self, provider, access, info):

        try:
            user =  User.objects.get(email=info['email'])
            if (user.has_default_picture()):
                self.try_adding_picture(info, user, provider)

            return user
        except User.DoesNotExist:
            kwargs = {
                User.USERNAME_FIELD: info['email'],
                'password': None,
                'name': info['name'],
                'login_type': self.get_login_type(provider),
            }

            user = User.objects.create_user(**kwargs)
            self.try_adding_picture(info, user, provider)
            return user

    def handle_existing_user(self, provider, user, access, info):
        if (user.has_default_picture()):
                self.try_adding_picture(info, user, provider)

        return super(CustomUserCallback, self).handle_existing_user(provider, user, access, info)

    def get_error_redirect(self, provider, reason):
        "Return url to redirect on login failure."
        return reverse('auth-failure', kwargs={'provider': provider.name})

    def get_login_redirect(self, provider, user, access, new=False):
        "Return url to redirect authenticated users."
        return reverse('auth-success', kwargs={'provider': provider.name})

def auth_success(request, provider):
    response = HttpResponse("Successfully logged in.....redirecting");
    response.set_cookie('userLoggedIn', provider);
    return response

def auth_failure(request, provider):
    response = HttpResponse("Failed to log in.....redirecting");
    response.set_cookie('userLoggedNot', provider);
    return response
