from django.urls import path
from apps.livechat import views

urlpatterns = [
    path('livechat/',views.lobby),
]
