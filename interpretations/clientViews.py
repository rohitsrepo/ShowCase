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
    	user = request.user,
        public = True
    )

    return redirect('/write-a-tale/drafts/' + str(draft.id))


@login_required
def edit_interpretation(request, id):
    interpretation = get_object_or_404(Interpretation, id=id)

    if interpretation.user.id != request.user.id:
        return redirect('arts/'+ interpretation.composition.slug +'/write-a-tale')

    composition = interpretation.composition
    context = RequestContext(request, {'composition': composition, 'interpretation': interpretation, 'editMode': True})
    return render_to_response("interpret.html", context)


def show_interpretation(request, user_slug, interpret_slug):
    interpretation = get_object_or_404(Interpretation, slug=interpret_slug, user__slug=user_slug)

    if interpretation.is_draft:
        return redirect('/write-a-tale/drafts/' + str(interpretation.id))

    if request.user.is_authenticated():
        user_id = request.user.id
    else:
        user_id = 0

    context = RequestContext(request, {
        'interpretation': interpretation,
        'composition': interpretation.composition,
        'is_me' : interpretation.user.id == user_id,
        'is_admired' : interpretation.is_admired(user_id),
        'is_bookmarked' : interpretation.is_bookmarked(user_id),
        'is_user_followed' : interpretation.user.is_followed(user_id),
        'editMode': False})
    return render_to_response("interpretation.html", context)
