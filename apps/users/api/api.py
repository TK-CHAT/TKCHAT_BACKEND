from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.users.api.serializers import AccountRegistrationSerializer,LoginSerializer,UserSerializer,pruebaSerializer
from rest_framework import status
from apps.users.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_auth_view(request, format=None):
  
  header= JWTAuthentication.get_header(self=JWTAuthentication,request=request)
  rawToken= JWTAuthentication.get_raw_token(self=JWTAuthentication,header=header)
  access_token = AccessToken(rawToken)
  user = access_token['user_id']
  content = {
    'status': 'Authenticated',
    'user': user,
  }
  return Response(content)
  
@api_view(['POST'])
def account_registration_view(request):
  if request.method == 'POST':
    serializer = AccountRegistrationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def account_login_view(request):
  if request.method == 'POST':
    serializer = LoginSerializer(data=request.data,context=request.data)
    if serializer.is_valid():
      context_token = serializer.get_context_token()
      return Response(context_token, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def account_info_view(request):
  if request.method == 'GET':
    se = pruebaSerializer(data=request.GET)
    print(se.is_valid())
    queryset = User.objects.all()
    queryset = User.objects.filter_by_user_id(request, queryset)
    serializer = UserSerializer(queryset,many=True)
    return Response(serializer.data,status=status.HTTP_202_ACCEPTED)