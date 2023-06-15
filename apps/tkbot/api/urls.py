from django.urls import path
from apps.tkbot.api.api import checkIA

urlpatterns = [
    path('init/',checkIA, name='init_'),
]
