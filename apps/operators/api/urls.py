from django.urls import path
from apps.operators.api.api import register_operato_view

urlpatterns = [
    path('register/',register_operato_view, name='operator_register'),
    # path('update/',company_update_view, name='company_update'),
]
