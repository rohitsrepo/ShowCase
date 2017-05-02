from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required

from .models import Interpretation

from compositions.models import Composition

@login_required
def add_interpretation(request, slug):
    composition = get_object_or_404(Composition, slug=slug)
    draft = Interpretation.objects.create(
    	composition = composition,
    	user = request.user
    )

    return redirect('/write-a-tale/drafts/' + str(draft.id))


@login_required
def edit_interpretation(request, id):
    interpretation = get_object_or_404(Interpretation, id=id)
    composition = interpretation.composition
    context = RequestContext(request, {'composition': composition, 'interpretation': interpretation, 'editMode': True})
    return render_to_response("interpret.html", context)


def show_interpretation(request, user_slug, interpret_slug):
    interpretation = get_object_or_404(Interpretation, slug=interpret_slug, user__slug=user_slug)
    context = RequestContext(request, {
        'interpretation': interpretation,
        'composition': interpretation.composition,
        'editMode': False})
    return render_to_response("interpretation.html", context)
