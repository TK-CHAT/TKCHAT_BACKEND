from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from apps.wsp.models import ClientWSP
from .serializers import WPSMessageSerializer,ClientWPSSerializer,ChatWSPSerializer,ChatWSPDefaultSerializer
from common.constants.constants import CHAT_STATUS,MSG_DESTINATION,MSG_ROL
from apps.wsp.models import ChatWSP,WSP
from django.views.decorators.csrf import csrf_exempt
from apps.companies.models import Company
from apps.tkbot.models import Bot
from apps.tkbot.api.serializers import botSerializer
from apps.tkbot.models import openAI

openIA_instance=openAI()

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
  client = ClientWSP.auto_check_add(sender.split(":")[1])
  try:
    company = Company.objects.get(phone= receiver.split(":")[1])
  except Company.DoesNotExist:
    print("No se encontro una compañia creado")
    return Response({"Company":"Company not found"},status=status.HTTP_400_BAD_REQUEST)
  auto_bot= Bot.get_user_bot(Bot,company)
  if not auto_bot:
    bot_serializer= botSerializer(data=Bot.get_register_query(Bot,company))
    if bot_serializer.is_valid():
      auto_bot=bot_serializer.save()
    else:
      print(bot_serializer.errors)
      return Response(bot_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
      
  chat = ChatWSP.check_get(ChatWSP,client=client)
  if not chat:
    query_chat = {
      "client":client.id,
      "operator":[auto_bot.id],
      "company":company.id,
    }
    serializer_chat = ChatWSPSerializer(data=query_chat)
    if serializer_chat.is_valid():
      chat = serializer_chat.save()
    else:
      print(serializer_chat.errors)
      return Response(serializer_chat.errors,status=status.HTTP_400_BAD_REQUEST)
  msg_query = {
    "msg":message,
    "chat":chat.id,
    "destiny":MSG_DESTINATION.COMPANY,
    "role":MSG_ROL.USER
  }
  msg_serializer = WPSMessageSerializer(data=msg_query)
  if msg_serializer.is_valid():
    msg = msg_serializer.save()
  else:
    print(msg_serializer.errors)
    return Response(msg_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  bot_response = openIA_instance.get_response_msg(message)
  # print(bot_response)
  response_msg=bot_response['choices'][0]['text']
  msg_response_query={
    "msg":response_msg,
    "chat":chat.id,
    "destiny":MSG_DESTINATION.CLIENT,
    "role":MSG_ROL.ASSISTANT
  }
  msg_response_serilizer= WPSMessageSerializer(data=msg_response_query)
  if msg_response_serilizer.is_valid():
    response_msg_valid = msg_response_serilizer.save()
    wps_instance = WSP()
    wps_instance.send_message(response_msg_valid)
  else:
    print(msg_response_serilizer.errors)
    return Response(msg_response_serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
  return Response({"Status":"OK"},status=status.HTTP_200_OK)
    