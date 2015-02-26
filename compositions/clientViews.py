from .models import Composition
from django.shortcuts import get_object_or_404, render_to_response



def composition_main(request, slug):
	composition = get_object_or_404(Composition, slug=slug)
	return render_to_response("composition.html", {'composition': composition})
