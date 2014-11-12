from rest_framework.test import APITestCase
from django.utils.timesince import timesince


class CommentsTest(APITestCase):

    "Base class for comments test."

    maxDiff = None

    def createResponse(self,
                       id,
                       comment,
                       commenter,
                       interpretation,
                       create_time,
                       edited=False):
        time_gap = timesince(create_time)
        return {'id': id,
                'comment': comment,
                'commenter': commenter,
                'interpretation': interpretation,
                'timesince': time_gap,
                'edited': edited}
