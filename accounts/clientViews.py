from .models import User
from django.shortcuts import get_object_or_404, render_to_response


def artist_main(request, slug):
	artist = get_object_or_404(User, slug=slug)
	return render_to_response("artist.html", {'artist': artist})
