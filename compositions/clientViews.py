from .models import Composition
from django.shortcuts import get_object_or_404, render_to_response


def composition_main(request, slug):
    composition = get_object_or_404(Composition, slug=slug)
    composition.views = composition.views + 1
    composition.save()
    try:
        top_interpretation = composition.interpretation_set.all()[0].to_text()
    except:
        top_interpretation = "Explore Art through Stories and Interpretations."
    return render_to_response("composition.html", {'composition': composition, 'top_interpretation': top_interpretation})

def add_interpretation(request, slug):
    composition = get_object_or_404(Composition, slug=slug)
    return render_to_response("interpret.html", {'composition': composition})
