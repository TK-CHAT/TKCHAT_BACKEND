from django.utils.deprecation import MiddlewareMixin
from django.http import QueryDict
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

BYPASSED_ROUTES = [
  '/api/account/register/',
  '/api/account/login/'
]

def get_user_id(request):
  header = JWTAuthentication.get_header(self=JWTAuthentication, request=request)
  rawToken = JWTAuthentication.get_raw_token(self=JWTAuthentication, header=header)
  access_token = AccessToken(rawToken)
  user_id = access_token['user_id']
  return user_id

class ModificarRequestMiddleware(MiddlewareMixin):
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    
    if request.path not in BYPASSED_ROUTES:
      user_id = get_user_id(request=request)
      if request.method == 'GET':
        get_data = request.GET.copy()
        get_data.update({'user_id': user_id})
        request.GET = get_data
        
      if request.method == 'POST':
        get_data = request.POST.copy()
        get_data.update({'user_id': user_id})
        request.POST = get_data
        
    response = self.get_response(request)
    return response
