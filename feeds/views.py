from django.conf import settings
from .models import StaffPost
from .serializers import PaginatedPostSerializer, PostSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from interpretations.models import Interpretation
from django.db.models import Q
from django.http import Http404

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def editors_pick_list(request, format=None):
    page_num = request.GET.get('page', 1)
    editors_posts = StaffPost.objects.all().order_by('-id')

    paginator = Paginator(editors_posts, 4)#settings.POSTS_PER_PAGE)

    try:
        this_page_posts = paginator.page(page_num)
    except PageNotAnInteger:
        this_page_posts = paginator.page(1)
    except EmptyPage:
        raise Http404

    serializer = PaginatedPostSerializer(this_page_posts)

    if request.user.is_authenticated():
        add_voting_status(this_page_posts, request.user, serializer.data['results'])

    add_comment_count(this_page_posts, serializer.data['results'])
    add_interpretation_rank(this_page_posts, serializer.data['results'])

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def editors_pick_next(request, format=None):
    post_id = request.GET.get('postId', 0)
    composition_id = request.GET.get('compositionId', 0)
    post_count = request.GET.get('count', 3)

    try :
        next_posts = StaffPost.objects.filter(~Q(composition__id = composition_id), Q(id__lt=post_id)).order_by('-id')[:post_count]
    except: 
        next_posts = default_editors_posts(composition_id, post_count)

    if (next_posts.count() == 0):
        next_posts = default_editors_posts(composition_id, post_count)

    serializer = PostSerializer(next_posts)
    return Response(serializer.data)

def default_editors_posts(composition_id, post_count):
    try:
        next_posts = StaffPost.objects.filter(~Q(composition__id = composition_id)).order_by('-id')[:post_count]
    except:
        next_posts = StaffPost.objects.all().order_by('-id')[:post_count]

    return next_posts;

def add_interpretation_rank(posts, results):
    counter=0
    for post in posts:
        results[counter]['interpretation_rank'] = Interpretation.objects.filter(composition=post.composition, id__lt=post.interpretation.id).count()
        counter += 1
   
def add_voting_status(posts, user, results):
    counter = 0;
    for post in posts:
        results[counter]['voting_status'] = post.interpretation.vote.get_voting_status(user)
        counter += 1

def add_comment_count(posts, results):
    counter = 0
    for post in posts:
        results[counter]['comments_count'] = post.interpretation.comments.count()
        counter += 1    
    
    

