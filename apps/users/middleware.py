from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response

from django.http import QueryDict
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from apps.users.api.serializers import UserIdSerializerModel
from rest_framework import status

BYPASSED_ROUTES = [
  '/api/account/register/',
  '/api/account/login/'
]

def get_user_id(request):
  try:
    header = JWTAuthentication.get_header(self=JWTAuthentication, request=request)
    rawToken = JWTAuthentication.get_raw_token(self=JWTAuthentication, header=header)
    access_token = AccessToken(rawToken)
    user_id = access_token['user_id']
    return user_id
  except:
    return None

class ModificarRequestMiddleware(MiddlewareMixin):
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    if request.path not in BYPASSED_ROUTES:
      print('check')
      user_id = get_user_id(request=request)
      user_serializer = UserIdSerializerModel(data={'id':user_id})
      if user_serializer.is_valid():
        request.user=user_id
      else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    response = self.get_response(request)
    return response
      

    
