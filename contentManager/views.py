from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from .models import ReportAbuse
from compositions.models import Composition


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def report_composition(request, format=None):
    compositionId = request.DATA.get('compositionId', 0)

    try:
        composition = Composition.objects.get(pk=compositionId)
        ReportAbuse.objects.create(composition = composition, reporter=request.user);
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
