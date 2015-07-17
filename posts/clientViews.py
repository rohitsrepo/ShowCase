from .models import Post
from django.shortcuts import get_object_or_404, render_to_response

def post_main(request, user_slug, post_id):
    post = get_object_or_404(Post, pk=post_id, creator__slug=user_slug)
    return render_to_response("post.html", {'post': post, 'user_slug': user_slug})
