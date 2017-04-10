from .models import Interpretation
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response


def show_interpretation(request, user_slug, interpret_slug):
    interpretation = get_object_or_404(Interpretation, slug=interpret_slug, user__slug=user_slug)
    context = RequestContext(request, {
        'interpretation': interpretation,
        'composition': interpretation.composition,
        'editMode': False})
    return render_to_response("interpretation.html", context)
