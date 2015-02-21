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

    paginator = Paginator(editors_posts, 2)#settings.POSTS_PER_PAGE)

    try:
        this_page_posts = paginator.page(page_num)
    except PageNotAnInteger:
        this_page_posts = paginator.page(1)
    except EmptyPage:
        this_page_posts = paginator.page(paginator.num_pages)

    serializer = PaginatedPostSerializer(this_page_posts)

    return Response(serializer.data)

   
    
    
    

