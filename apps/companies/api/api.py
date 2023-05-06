from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from apps.companies.api.serializers import CompanyUpdateDataSerializer,CompanySerializer
from rest_framework import status
from apps.companies.models import Company

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def company_registration_view(request):
  if request.method == 'POST':
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def company_update_view(request):
  if request.method == 'POST':
    try:  
      instance = Company.objects.get(id=request.data['id'])
      serializer = CompanyUpdateDataSerializer(instance=instance, data=request.data, partial=True, context=instance)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
      context_error = {
        'id': 'Company not found'
      }
      return Response(context_error, status=status.HTTP_400_BAD_REQUEST)
