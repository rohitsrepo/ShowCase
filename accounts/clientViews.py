from .models import User
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

def site_main(request):
    context = RequestContext(request)
    return render_to_response("reader.html", context)

def artist_main(request, slug):
    artist = get_object_or_404(User, slug=slug)
    is_followed = artist.is_followed(request.user.id)

    context = RequestContext(request, {'artist': artist, 'is_followed': is_followed})
    return render_to_response("user_profile.html", context)


def user_settings(request):
    if not request.user.is_authenticated:
        raise Http404

    context = RequestContext(request)
    return render_to_response("user_settings.html", context)