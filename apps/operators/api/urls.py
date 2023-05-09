from django.urls import path
from apps.operators.api.api import register_operator_view,update_operator_view

urlpatterns = [
    path('register/',register_operator_view, name='operator_register'),
    path('update/',update_operator_view, name='operator_update'),
]
