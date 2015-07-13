from .models import Post
from .serializers import PostSerializer, PaginatedPostSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from accounts.models import User


class CompositionPostList(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	def get(self, request, composition_id, format=None):
		posts = Post.objects.filter(composition_id = composition_id)
		serializer = PostSerializer(posts, context={'request': request})
		return Response(serializer.data)

class UserPostList(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	def get(self, request, user_id, format=None):
		user = get_object_or_404(User, pk=user_id)
		user_posts = user.user_posts.all().order_by('-id')

		page_num = request.GET.get('page', 1)
		paginator = Paginator(user_posts, 9)

		try:
		    this_page_posts = paginator.page(page_num)
		except PageNotAnInteger:
		    this_page_posts = paginator.page(1)
		except EmptyPage:
		    raise Http404

		serializer = PaginatedPostSerializer(this_page_posts, context={'request': request})
		return Response(data=serializer.data)

