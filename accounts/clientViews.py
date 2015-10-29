from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .models import User

def site_main(request):
    if request.user.is_authenticated():
        return redirect('/home')
    else:
        context = RequestContext(request)
        return render_to_response("reader.html", context)

def artist_main(request, slug):
    artist = get_object_or_404(User, slug=slug)
    is_followed = artist.is_followed(request.user.id)

    is_me = False
    if request.user.id == artist.id:
        is_me = True

    context = RequestContext(request, {'artist': artist, 'is_followed': is_followed, 'is_me': is_me})
    return render_to_response("user_profile.html", context)

def profile_main(request):
    artist = get_object_or_404(User, id=request.user.id)
    is_followed = artist.is_followed(request.user.id)
    context = RequestContext(request, {'artist': artist, 'is_followed': is_followed})
    return render_to_response("user_profile.html", context)

@login_required
def user_settings(request):
    if not request.user.is_authenticated:
        raise Http404

    context = RequestContext(request)
    return render_to_response("user_settings.html", context)

def register_main(request):
    if request.user.is_authenticated():
        return redirect('/home')
    else:
        context = RequestContext(request)
        return render_to_response("register.html", context)

def login_main(request):
    if request.user.is_authenticated():
        return redirect('/home')
    else:
        context = RequestContext(request)
        return render_to_response("login.html", context)

def reset_password_confirm(request, uidb64, token, format=None):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        context = RequestContext(request, {'page_type': 'reset_password_confirm', 'id': uidb64, 'token': token})
        return render_to_response("reset-password.html", context)
    else:
        context = RequestContext(request, {'page_type': 'reset_password_confirm_error'})
        return render_to_response("reset-password.html", context)

    

    