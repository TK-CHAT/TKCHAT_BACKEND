from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from apps.wsp.models import WSP,ClientWSP
from .serializers import WPSMessageSerializer,ClientWPSSerializer,ChatWSPSerializer,ChatWSPDefaultSerializer
from django.db import IntegrityError
from common.constants.constants import CHAT_STATUS,MSG_DESTINATION,MSG_ROL
from apps.wsp.models import ChatWSP,MessageWSP
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from apps.companies.models import Company
from apps.tkbot.models import Bot

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
  
@api_view(['GET'])
def delete_chat_view(request, pk):
    try:
        print(pk)
        chat = ChatWSP.objects.get(pk=pk)
        chat.delete()
    except ChatWSP.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
@csrf_exempt
def receive_msg_wps_view(request):
  sender = request.POST.get('From')
  receiver = request.POST.get('To')
  message = request.POST.get('Body')
  print(f'{sender} says {message}')
  print(request.POST)
  client = ClientWSP.auto_check_add(sender.split(":")[1])
  try:
    company = Company.objects.get(phone= receiver.split(":")[1])
    auto_bot= Bot()
    if not auto_bot.exist():
      auto_bot.create()
    auto_bot= auto_bot.get_user_bot()
    chat = ChatWSP.auto_check_add(client=client,company=company,bot=auto_bot)
    msg = MessageWSP.objects.create(
      msg=message,
      chat=chat,
      status=MSG_DESTINATION.COMPANY,
      role = MSG_ROL.USER
    )
  except Company.DoesNotExist:
    print("La compañia no funca :C")
  
  return Response({"Status":"OK"},status=status.HTTP_200_OK)
    