from django.shortcuts import render
from django.conf import settings
from .models import EditorsListPost, FeedPost
from .serializers import FeedPostSerializer, PaginatedFeedPostSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.pagination import PaginationSerializer
from interpretationVotes.models import InterpretationVote


def populate_list_Editors_pick(list_Editors_pick):
    list_EditorsPosts = EditorsListPost.objects.all()
    if(len(list_EditorsPosts) != 0 ):
        for index in range(len(list_EditorsPosts)):
            objectFeedPost = FeedPost()
            objectFeedPost.id = index+1
            objectFeedPost.painting_image = list_EditorsPosts[index].composition.matter
            objectFeedPost.painting_name = list_EditorsPosts[index].composition.title
            objectFeedPost.painter = list_EditorsPosts[index].composition.artist.get_full_name()
            objectFeedPost.interpretation = list_EditorsPosts[index].interpretation.interpretation
            objectFeedPost.interpretation_writer = list_EditorsPosts[index].interpretation.user.get_full_name()
            objectFeedPost.interpretation_votes = InterpretationVote.objects.get(interpretation = list_EditorsPosts[index].interpretation).positive
            list_Editors_pick.append(objectFeedPost)
    return list_Editors_pick


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def editors_pick_list(request, format=None):
    #initialize required data
    page_num = request.DATA['page_num']
    FeedPost.objects.all().delete()
    list_Editors_pick_feed = []
    #get relevant data
    # list_Editors_pick contains list of FeedPost objects
    list_Editors_pick_feed = populate_list_Editors_pick(list_Editors_pick_feed)
    #count maximum number of pages needed
    num_editors_pick = len(list_Editors_pick_feed)
    max_pages = (num_editors_pick/settings.PAGE_POST_CONTENT_LIMIT) + 1
    #pagination
    paginator = Paginator(list_Editors_pick_feed, max_pages)
    try:
        this_page_content = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        this_page_content = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        this_page_content = paginator.page(paginator.num_pages)
    #setting up serializer
    serializer_context = {'request': request}
    serializer = PaginatedFeedPostSerializer(this_page_content, context=serializer_context)
    return Response(serializer.data)    
    
    
    

