from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from apps.companies.api.serializers import CompanyUpdateDataSerializer,CompanySerializer, ValidCompanySerializer
from rest_framework import status
from apps.tkbot.models import openAI



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def checkIA(request):
  if request.method == 'POST':
    print("GOOOO")
    res = openAI()
    
    return Response({'status':'OK'}, status=status.HTTP_200_OK)

    
