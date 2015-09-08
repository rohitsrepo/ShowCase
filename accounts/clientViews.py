from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required

from .models import User

def site_main(request):
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