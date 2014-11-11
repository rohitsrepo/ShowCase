from rest_framework.test import APITestCase
from django.utils.timesince import timesince


class InterpretationsTest(APITestCase):

    "Base class for interpretations test."

    maxDiff = None

    def createResponse(self,
                       id,
                       interpretation,
                       user,
                       composition,
                       create_time):
        time_gap = timesince(create_time)
        return {'id': id,
                'interpretation': interpretation,
                'user': user,
                'composition': composition,
                'timesince': time_gap}
