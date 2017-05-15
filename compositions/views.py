import os, uuid
import json
import urllib
from random import randrange, randint

import django_filters
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template.defaultfilters import slugify
from django.core.files import File

from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import Composition, InterpretationImage, TemporaryComposition
from .serializers import CompositionSerializer, NewCompositionSerializer, EditCompositionSerializer, CompositionMatterSerializer, InterpretationImageSerializer, PaginatedCompositionSerializer
from .permissions import IsOwnerOrReadOnly, IsHimself, IsImageUploader
from .imageTools import crop

from accounts.models import User
from accounts.serializers import ExistingUserSerializer
from buckets.serializers import BucketSerializer
from buckets.models import BucketMembership
from feeds.models import Fresh
from interpretations.serializers import InterpretationSerializer
from mediastore.manager import upload_image
from ShowCase.utils import check_object_permissions, BrowserSimulator

class CompositionError(Exception):
    pass


def get_image_path(user, name):
    relative_path = '../media/temp/' + user.slug + '/' + name + '.jpg'
    return os.path.join(settings.BASE_DIR, relative_path)


def get_image_object(user, name):
    url = '/media/temp/' + user.slug + '/' + name + '.jpg'
    id = name

    return {'url': url, 'id': id}

def get_image_from_web(image_url, image_path):
    opener = BrowserSimulator()
    opener.retrieve(image_url, image_path)

def get_image_from_upload(image_file, image_path):
    with open(image_path, 'wb') as dest:
        for chunk in image_file.chunks():
            dest.write(chunk)

def generate_image_url(user, upload_object):
    image_name = str(uuid.uuid1())
    image_path = get_image_path(user, image_name)

    if not os.path.exists(os.path.dirname(image_path)):
        os.makedirs(os.path.dirname(image_path))

    if (upload_object['upload_type'] == 'url'):
        get_image_from_web(upload_object['upload_url'], image_path)
    elif (upload_object['upload_type'] == 'upl'):
        get_image_from_upload(upload_object['upload_image'], image_path)

    return get_image_object(user, image_name)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def composition_matter(request, format=None):
    upload_ser = CompositionMatterSerializer(data=request.DATA, files=request.FILES, context={'request': request})

    if upload_ser.is_valid():
        image_object = generate_image_url(request.user, upload_ser.object)
        temp_image = TemporaryComposition.objects.create(identifier=image_object['id'], owner=request.user)
        image_object['id'] = temp_image.id
        return Response(image_object)

    return Response(data=upload_ser.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def generate_matter(self, temp_image):
        image_path = get_image_path(temp_image.owner, temp_image.identifier)
        return File(open(image_path))

    def get_valid_bucket(self, user, request_data):
        if ('bucket' in request_data.keys()):
            bucket_id = request_data['bucket']
            try:
                return user.buckets.get(id=bucket_id)
            except:
                return False
        else:
            return False

    def addToBucket(self, bucket, composition):
        BucketMembership.objects.get_or_create(bucket=bucket, composition=composition)

    def remove_temp_image(self, temp_image):
        image_path = get_image_path(temp_image.owner, temp_image.identifier)
        os.remove(image_path)

    def get_public_id(self, uploader, artist, composition_name):
        return '%s/%s/%s_%s_thirddime_%s' % (slugify(uploader.name),
            slugify(artist.name),
            slugify(artist.name),
            slugify(composition_name),
            randint(1000, 10000))

    def post(self, request, format=None):
        try:
            if not ('image_id' in request.DATA.keys()):
                return Response(data={"error": "image_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            temp_image = get_object_or_404(TemporaryComposition, id=request.DATA['image_id'], owner=request.user, pristine=True)
            matter = self.generate_matter(temp_image)
            request.DATA['matter'] = matter

            self.validate_or_create_artist(request.DATA)

            ser = NewCompositionSerializer(data=request.DATA, files=request.FILES, context={'request': request})

            if ser.is_valid():
                bucket = self.get_valid_bucket(request.user, request.DATA)
                if bucket:
                    ser.object.added_with_bucket = True

                matter_public_id = self.get_public_id(request.user, ser.object.artist, ser.object.title)
                matter_meta = upload_image(matter, public_id=matter_public_id, phash = True, eager = [{ 'width': 550}, { 'width': 400}])

                ser.object.uploader = request.user
                ser.object.matter_identifier = matter_meta['public_id']
                ser.object.matter_height = matter_meta['height']
                ser.object.matter_width = matter_meta['width']
                ser.object.matter_format = matter_meta['format']
                ser.object.matter_phash = matter_meta['phash']

                composition = ser.save()

                temp_image.pristine = False
                temp_image.save()

                self.remove_temp_image(temp_image)

                if bucket:
                    self.addToBucket(bucket, composition)
                return Response(ser.data, status=status.HTTP_201_CREATED)

            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except CompositionError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

class CompositionDetail(APIView):
    '''Handel endpoints for individual composition.'''

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

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

    def get_composition(self, slug, request):
        try:
            composition = Composition.objects.get(slug=slug)
            check_object_permissions(request, self.permission_classes, composition)
            return composition
        except Composition.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        composition = self.get_composition(slug, request)
        ser = CompositionSerializer(composition, context={'request': request})
        return Response(ser.data)

    def put(self, request, slug, format=None):
        composition = self.get_composition(slug, request)
        self.check_object_permissions(self.request, composition)

        self.validate_or_create_artist(request.DATA)

        ser = EditCompositionSerializer(composition, data=request.DATA, context={'request': request})

        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


    ## Deletes more than the composition
    ## Also delete the buckets it does not even belong to
    ## Use background job architecture to delete

    def delete(self, request, slug, format=None):
        composition = self.get_composition(slug, request)
        self.check_object_permissions(self.request, composition)
        Fresh.objects.get(feed_type=Fresh.ART,
            object_id=composition.id).delete()
        composition.bookers.all().delete()
        composition.admirers.all().delete()
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
def get_associates(request, composition_id, format=None):
    composition = get_object_or_404(Composition, pk=composition_id)
    artBuckets = composition.holders.filter(public=True).order_by('-views')[:3]
    artistWorks = composition.artist.arts.exclude(id=composition_id).order_by('-created')[:4]
    uploaderWorks = composition.uploader.compositions.exclude(id=composition_id).exclude(artist=composition.artist).order_by('-created')[:4]
    artInterprets = composition.interprets.filter(public=True, is_draft=False).order_by('-created')

    artBucketsCount = composition.holders.count()
    artistWorksCount = composition.artist.arts.count()
    uploaderWorksCount = composition.uploader.compositions.count()
    artInterpretsCount = composition.interprets.count()

    artBucketsSerializer = BucketSerializer(artBuckets, context={'request': request})
    artistWorksSerializer = CompositionSerializer(artistWorks, context={'request': request})
    uploaderWorksSerializer = CompositionSerializer(uploaderWorks, context={'request': request})
    artInterpretsSerializer = InterpretationSerializer(artInterprets, context={'request': request})

    result = {'artBuckets': artBucketsSerializer.data,
    'artInterprets': artInterpretsSerializer.data,
    'artistWorks': artistWorksSerializer.data,
    'uploaderWorks': uploaderWorksSerializer.data,
    'counts': {'artBuckets': artBucketsCount,
        'artInterprets': artInterpretsCount,
        'artistWorks': artistWorksCount,
        'uploaderWorks': uploaderWorksCount
    }}

    return Response(result)
