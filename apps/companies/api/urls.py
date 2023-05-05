from django.urls import path
from apps.companies.api.api import company_registration_view,company_update_view

urlpatterns = [
    path('register/',company_registration_view, name='company_register'),
    path('update/',company_update_view, name='company_update'),
]
