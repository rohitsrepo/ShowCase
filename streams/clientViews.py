from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

@login_required()
def posts_main(request):
    context = RequestContext(request, {})
    return render_to_response("myposts.html", context)
