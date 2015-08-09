import os, django_filters
from django.db.models import Q
from .models import Composition, InterpretationImage
from accounts.models import User
from rest_framework import permissions, generics, status
from .serializers import CompositionSerializer, NewCompositionSerializer, InterpretationImageSerializer, PaginatedCompositionSerializer, BookmarkerSerializer
from .permissions import IsOwnerOrReadOnly, IsHimself, IsImageUploader
from buckets.serializers import BucketSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import Http404
from accounts.serializers import ExistingUserSerializer
from rest_framework.decorators import api_view, permission_classes
from ShowCase.utils import check_object_permissions
from .imageTools import crop
from django.core.files import File
from random import randrange
import json

class CompositionError(Exception):
    pass

class CompositionList(APIView):
    ''' Handels listing of compositions and adding new ones.'''
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def is_number(self, string_val):
        try:
            int(float(string_val))
            return True
        except ValueError:
            return False

    def validate_or_create_artist(self, request_data):
        artist = request_data.get('artist')
        if not self.is_number(artist):
            try:
                artist = json.loads(artist)
                if artist.get('id') == -1:
                    artist_name = artist.get('name')
                    matching_artists = User.objects.filter(name__iexact=artist_name)

                    if not matching_artists:
                        new_artist = User.objects.create_artist(artist_name)
                        request_data['artist'] = new_artist.id
                    else:
                        request_data['artist'] = matching_artists[0].id
                else:
                    raise CompositionError("Invalid artist data {}".format(artist))
            except:
                raise CompositionError("Unable to parse artist data {}".format(artist))


    def get(self, request, format=None):
        compositions = Composition.objects.all()
        ser = CompositionSerializer(compositions, many=True)

        if request.user.is_authenticated():
            counter = 0
            related_comps = compositions.filter(bookers__id=request.user.id)
            for composition in compositions:
                ser.data[counter]['IsBookmarked'] = False
                # ser.data[counter]['IsVoted'] = False

                if composition in related_comps:
                    ser.data[counter]['IsBookmarked'] = True
                # if request.user.votes.filter(composition=composition).exists():
                #     ser.data[counter]['IsVoted'] = True
                counter = counter + 1
        return Response(ser.data)

    def post(self, request, format=None):
        try:
            self.validate_or_create_artist(request.DATA)
            ser = NewCompositionSerializer(data=request.DATA, files=request.FILES, context={'request': request})
            if ser.is_valid():
                ser.object.uploader = request.user
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)

            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except CompositionError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


class CompositionDetail(APIView):
    '''Handel endpoints for individual composition.'''

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_composition(self, pk, request):
        try:
            composition = Composition.objects.get(pk=pk)
            check_object_permissions(request, self.permission_classes, composition)
            return composition
        except Composition.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        composition = self.get_composition(pk, request)
        ser = CompositionSerializer(composition)
        ser.data['IsBookmarked'] = False
        ser.data['IsVoted'] = False
        if(composition.bookers.filter(pk=request.user.id).exists()):
            ser.data['IsBookmarked'] = True
        if request.user.is_authenticated() and request.user.votes.filter(composition=composition).exists():
            ser.data['IsVoted'] = True

        return Response(ser.data)

    def put(self, request, pk, format=None):
        composition = self.get_composition(pk, request)
        ser = CompositionSerializer(composition, data=request.DATA, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        composition = self.get_composition(pk, request)
        composition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InterpretationImageList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, composition_id, format=None):
        composition = get_object_or_404(Composition, pk=composition_id)
        images = InterpretationImage.objects.filter(composition=composition)
        serializer = InterpretationImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, composition_id, format=None):
        composition = get_object_or_404(Composition, pk=composition_id)

        source_type = request.DATA.get('source_type')
        if source_type and source_type == InterpretationImage.CROP:
            return self._cropAndCreate(request, composition)

        return self._addImage(request, composition)

    def _cropAndCreate(self, request, composition):
        try:
            cropped_file_path = crop(composition.matter.path, tuple(request.DATA.get('box')))
            with open(cropped_file_path) as cropped_file:
                interpret_image = InterpretationImage(image=File(cropped_file), composition=composition, uploader=request.user)
                interpret_image.save()

            os.remove(cropped_file_path)

            serializer = InterpretationImageSerializer(interpret_image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def _addImage(self, request, composition):
        serializer = InterpretationImageSerializer(data=request.DATA, files=request.FILES, context={'request': request})
        if serializer.is_valid():
            serializer.object.uploader = request.user
            serializer.object.composition = composition
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InterpretationImageDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, IsImageUploader)

    def delete(self, request, composition_id, image_id, format=None):
        interpretationImage = get_object_or_404(InterpretationImage, pk=image_id, composition_id=composition_id)
        interpretationImage.delete();

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, IsHimself))
def follow_compositions(request, format=None):
    check_object_permissions(request, follow_compositions.cls.permission_classes, request.user)
    follows = request.user.follows.all()
    if follows:
        q_object = Q()
        for follow in follows:
            q_object |= Q(uploader_id=follow.id)

    compositions = Composition.objects.filter(q_object)
    ser = CompositionSerializer(compositions, many=True)

    if request.user.is_authenticated():
        counter = 0
        related_comps = compositions.filter(bookers__id=request.user.id)
        for composition in compositions:
            ser.data[counter]['IsBookmarked'] = False
            ser.data[counter]['IsVoted'] = False

            if composition in related_comps:
                ser.data[counter]['IsBookmarked'] = True
            if request.user.votes.filter(composition=composition).exists():
                ser.data[counter]['IsVoted'] = True
            counter = counter + 1
        return Response(ser.data)
    return Response([])


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def random_composition(request, format=None):
    composition_count = Composition.objects.latest('created').id

    while 1:
        try:
            composition_id = randrange(1, composition_count+1)
            composition = Composition.objects.get(pk=composition_id)
            break
        except Composition.DoesNotExist:
            pass

    serializer = CompositionSerializer(composition)
    serializer.data['IsBookmarked'] = False
    serializer.data['IsVoted'] = False

    if request.user.is_authenticated():
        if (composition.bookers.filter(pk=request.user.id).exists()):
            serializer.data['IsBookmarked'] = True
        if request.user.votes.filter(composition=composition).exists():
            serializer.data['IsVoted'] = True

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_bookmarkers(request, composition_id, format=None):
    composition = get_object_or_404(Composition, pk=composition_id)
    bookers = composition.bookers.all()
    serializer = BookmarkerSerializer(bookers, context={'request': request})
    return Response(data=serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_buckets(request, composition_id, format=None):
    composition = get_object_or_404(Composition, pk=composition_id)
    buckets = composition.holders.all()
    serializer = BucketSerializer(buckets, context={'request': request})
    return Response(data=serializer.data)