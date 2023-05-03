from django.urls import path
from apps.companies.api.api import company_registration_view

urlpatterns = [
    path('register/',company_registration_view, name='company_register'),
]
