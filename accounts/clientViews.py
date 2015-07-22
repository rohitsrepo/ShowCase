from .models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response

def site_main(request):
    return render_to_response("reader.html", {"user": request.user})

def artist_main(request, slug):
	artist = get_object_or_404(User, slug=slug)
	return render_to_response("user_profile.html", {'artist': artist, 'user': request.user})


def user_settings(request):
    if not request.user.is_authenticated:
        raise Http404

    return render_to_response("user_settings.html", {'user': request.user})