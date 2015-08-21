from .models import Post
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

def posts_main(request, user_slug, post_id):
    post = get_object_or_404(Post, pk=post_id, creator__slug=user_slug)
    context = RequestContext(request, {'post': post, 'user_slug': user_slug})
    return render_to_response("posts.html", context)
