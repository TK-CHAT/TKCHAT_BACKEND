from django.urls import path
from apps.tkbot.api.api import checkIA,create_prompt_view,edit_prompt_view,delete_prompt_view

urlpatterns = [
    path('init/',checkIA, name='init_'),
    path('prompt/create/',create_prompt_view, name='create_prompt'),
    path('prompt/edit/',edit_prompt_view, name='edit_prompt'),
    path('prompt/delete/<int:pk>/',delete_prompt_view, name='delete_prompt'),
]
