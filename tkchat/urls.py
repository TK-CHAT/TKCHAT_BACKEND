"""
URL configuration for tkchat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/',jwt_views.TokenObtainPairView.as_view(), name='token_refresh'),
    path('api/account/',include('apps.users.api.urls')),
    path('api/companies/',include('apps.companies.api.urls')),
    path('api/operators/',include('apps.operators.api.urls')),
    path('api/livechat/',include('apps.livechat.api.urls')),
    path('api/wsp/',include('apps.wsp.api.urls')),
    path('api/tkbot/',include('apps.tkbot.api.urls')),
    
]
