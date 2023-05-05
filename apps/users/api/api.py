from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.users.api.serializers import UserAdminRegistrationSerializer,LoginSerializer,UserDataSerializer,UserIdSerializer
from rest_framework import status
from apps.users.models import User


"""
  Registro de usuario 
"""
@api_view(['POST'])
def account_registration_view(request):
  if request.method == 'POST':
    serializer = UserAdminRegistrationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
  Login de usuario 
"""
@api_view(['POST'])
def account_token_view(request):
  if request.method == 'POST':
    serializer = LoginSerializer(data=request.data,context=request.data)
    if serializer.is_valid():
      context_token = serializer.get_context_token()
      return Response(context_token, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
  Información del usuario 
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_info_view(request):
  if request.method == 'GET':
    serializer_user_id = UserIdSerializer(data=request.GET)
    if serializer_user_id.is_valid():
      queryset = User.objects.filter(id=serializer_user_id.validated_data['user_id'])
      serializer_response = UserDataSerializer(queryset,many=True)
      return Response(serializer_response.data,status=status.HTTP_202_ACCEPTED)
    return Response(serializer_user_id.errors,status=status.HTTP_401_UNAUTHORIZED)