from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from apps.wsp.models import WSP,ClientWSP
from .serializers import WPSMessageSerializer,ClientWPSSerializer,ChatWSPSerializer,ChatWSPDefaultSerializer
from django.db import IntegrityError
from common.constants.constants import CHAT_STATUS
from apps.wsp.models import ChatWSP


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def send_message_view(request):
  if request.method == 'POST':
    cliObj=None;
    try:
      cliObj = ClientWSP.objects.get(phone_number = request.data['phone_number'])
    except :
      clientSerializer = ClientWPSSerializer(data=request.data)
      if clientSerializer.is_valid():
        cliObj = clientSerializer.save()      
      return Response(clientSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    cliObj = ClientWSP.objects.get(phone_number = request.data['phone_number'])
    parseData = {
      'msg':request.data['message'],
      'send_by':2,
      'send_to':cliObj.id,
      'chat': 1,
    }
    serializer = WPSMessageSerializer(data=parseData)
    if serializer.is_valid():
      # msgObj = serializer.save()
      # wps = WSP()
      # wps.send_message(msgObj)
      return Response({'Status':'Ok'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat_view(request):
  if request.method == 'POST':
    serializer = ChatWSPSerializer(data=request.data)
    if serializer.is_valid():
      data = serializer.save()
      data.status = CHAT_STATUS.CREATE
      return Response(data, status=status.HTTP_201_CREATED)
    else: 
      try:
        chatObj = ChatWSP.objects.get(client=request.data['client'])
        alterSerializer = ChatWSPDefaultSerializer(chatObj)
        return Response(alterSerializer.data, status=status.HTTP_200_OK)
      except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
      