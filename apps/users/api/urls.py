from django.urls import path
from apps.users.api.api import account_registration_view,account_login_view,debug_auth_view


urlpatterns= [
  path('register/',account_registration_view,name='user_regiter'),
  path('login/',account_login_view,name='user_login'),
  path('debug/',debug_auth_view,name='user_debug'),
  
]