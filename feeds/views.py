from django.conf import settings
from .models import StaffPost
from .serializers import PaginatedPostSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def editors_pick_list(request, format=None):
    page_num = request.GET.get('page', 1)
    editors_posts = StaffPost.objects.all()

    paginator = Paginator(editors_posts, 4)#settings.POSTS_PER_PAGE)

    try:
        this_page_posts = paginator.page(page_num)
    except PageNotAnInteger:
        this_page_posts = paginator.page(1)
    except EmptyPage:
        this_page_posts = paginator.page(paginator.num_pages)

    serializer = PaginatedPostSerializer(this_page_posts)

    if request.user.is_authenticated():
        add_voting_status(this_page_posts, request.user, serializer.data['results'])

    add_comment_count(this_page_posts, serializer.data['results'])

    return Response(serializer.data)

   
def add_voting_status(posts, user, results):
    counter = 0;
    for post in posts:
        results[counter]['voting_status'] = post.interpretation.vote.get_voting_status(user)
        counter += 1

def add_comment_count(posts, results):
    counter = 0
    for post in posts:
        results[counter]['comments_count'] = post.interpretation.comment_set.count()
        counter += 1    
    
    

