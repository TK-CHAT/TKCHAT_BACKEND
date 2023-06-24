from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from apps.companies.api.serializers import CompanyUpdateDataSerializer,CompanySerializer, ValidCompanySerializer
from rest_framework import status
from apps.companies.models import Company
from apps.users.permissions import IsAdmin

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def company_registration_view(request):
  if request.method == 'POST':
    query = request.data.copy()
    query.update({'user': request.user.id})
    serializer = CompanySerializer(data=query)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def company_update_view(request):
  if request.method == 'POST':
    query = request.data.copy()
    query.update({'user': request.user.id})
    valid_company =  ValidCompanySerializer(data=query)
    if valid_company.is_valid():
      instance = Company.objects.get(id=query['id'])
      update_serializer = CompanyUpdateDataSerializer(instance=instance, data=query, partial=True, context=instance)
      if update_serializer.is_valid():
        update_serializer.save()
        return Response(update_serializer.data,status=status.HTTP_202_ACCEPTED)
      return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(valid_company.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdmin])
def get_bot_view(request, pk):
  try:
    company = Company.objects.get(id=pk)
    query = company.get_query_bot()
    print(query)
    return Response(query, status=status.HTTP_200_OK)
  except Company.DoesNotExist:
    return Response({'company_id': 'La empresa no existe'},status=status.HTTP_400_BAD_REQUEST)
  except:
    return Response({'company_id': 'La empresa no tienen un bot asignado'},status=status.HTTP_400_BAD_REQUEST)
