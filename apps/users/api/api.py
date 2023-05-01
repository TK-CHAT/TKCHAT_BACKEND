from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.users.api.serializers import AccountRegistrationSerializer,LoginSerializer
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


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def operator_api_view(request):
  
#   if request.method == 'GET':
#     operator = Operator.objects.all()
#     operator_serializer = OperatorSerializer(operator,many=True)
#     return Response(operator_serializer.data)
    
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
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
      user = User.objects.filter(email=request.data['email'])[0]
      contextToken = user.generate_context_token()
      return Response(contextToken)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)