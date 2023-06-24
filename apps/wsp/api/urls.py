from django.urls import path
from apps.wsp.api.api import send_message_view,create_chat_view,receive_msg_wps_view,delete_chat_view

urlpatterns = [
    path('chat/send_message/',send_message_view, name='send_message'),
    path('chat/create/',create_chat_view, name='create_chat'),
    path('chat/receive_msg/',receive_msg_wps_view, name='receive_msg_chat'),
    path('chats/delete/<int:pk>/', delete_chat_view, name='delete_chat'),
]
