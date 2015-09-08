from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from .models import Composition
from .serializers import PaginatedCompositionSerializer


def get_explore_paginator():
    compositions = Composition.objects.all().order_by('-id')
    paginator = Paginator(compositions, 15)
    return paginator

# def explore_main(request):
# 	paginator = get_explore_paginator()
# 	arts = paginator.page(1).object_list
# 	return render_to_response('explore.html', {'arts': arts})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_explores(request, format=None):
    page_num = request.GET.get('page', 1)
    paginator = get_explore_paginator()

    try:
        this_page_compositions = paginator.page(page_num)
    except PageNotAnInteger:
        this_page_compositions = paginator.page(1)
    except EmptyPage:
        raise Http404

    serializer = PaginatedCompositionSerializer(this_page_compositions, context={'request': request})
    return Response(data=serializer.data)
