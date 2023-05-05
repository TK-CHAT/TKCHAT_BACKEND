from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from apps.companies.api.serializers import CompanyRegistrationSerializer,CompanyDataSerializer
from apps.users.api.serializers import UserIdSerializer
from rest_framework import status
from apps.users.models import User

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def company_registration_view(request):
  
  if request.method == 'POST':
    serializer = CompanyRegistrationSerializer(data=request.data, context = request)
    if serializer.is_valid():
      user_queryset = User.objects.all()
      user_list = User.objects.filter_by_user_id(request=request, queryset=user_queryset)
      if len(user_list)==0:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      user_owner = user_list[0]
      serializer.save(user_owner)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def company_update_view(request):
  if request.method == 'POST':
    serializer_user_id =  UserIdSerializer(data=request.data)
    if serializer_user_id.is_valid():
      instance = User.objects.get(id=serializer_user_id.validated_data['user_id'])
      serializer_company = CompanyDataSerializer(instance=instance, data=request.data, partial=True)
      if serializer_company.is_valid():
        serializer_company.save()
        return Response(serializer_company.data,status=status.HTTP_202_ACCEPTED)
      return Response(serializer_company.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer_user_id.errors, status=status.HTTP_401_UNAUTHORIZED)
    

      