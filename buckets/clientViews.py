from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from .models import Bucket

def series_main(request, user_slug, bucket_slug):

    try:
        bucket = Bucket.objects.get(slug=bucket_slug, owner__slug=user_slug)
    except Bucket.DoesNotExist:
        raise Http404

    is_bookmarked = bucket.is_bookmarked(request.user.id)
    is_admired = bucket.is_admired(request.user.id)
    has_ownership = bucket.has_ownership(request.user.id)

    open_graph_images = [composition.matter.url for composition in bucket.compositions.all().order_by('-bucketmembership__added')[:5]]

    is_me = False
    if request.user.id == bucket.owner.id:
        is_me = True

    context = RequestContext(request, {'bucket': bucket,
     'is_me': is_me,
     'has_ownership': has_ownership,
     'is_bookmarked': is_bookmarked,
     'is_admired': is_admired,
     'open_graph_images': open_graph_images})
    return render_to_response("bucket.html", context)