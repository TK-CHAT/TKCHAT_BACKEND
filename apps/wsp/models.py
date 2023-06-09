from django.db import models
from apps.users.models import User
from apps.companies.models import Company
from common.constants.constants import CHAT_STATUS,MSG_DESTINATION,MSG_ROL
from twilio.rest import Client
import environ
env = environ.Env()
environ.Env.read_env()
import os


class ClientWSP(models.Model):
  phone_number = models.CharField(max_length=15, unique=True)
  client_name = models.CharField(max_length=60, null=True)
  start_connection = models.DateTimeField(auto_now_add=True)
  last_connection = models.DateTimeField(auto_now_add=True)
  REQUIRED_FIELDS = ['phone_number']
  def __str__(self) -> str:
    return str(self.phone_number)
  
  def auto_check_add(phone_number):
    try:
      client = ClientWSP.objects.get(phone_number=phone_number)
      if client:
        return client
      return None
    except ClientWSP.DoesNotExist: 
      client = ClientWSP.objects.create(phone_number=phone_number)
      return client

class ChatWSP(models.Model):
  client = models.OneToOneField(ClientWSP,on_delete=models.CASCADE)
  operator = models.ManyToManyField(User)
  creation_on = models.DateTimeField(auto_now_add=True)
  company = models.ForeignKey(Company,on_delete=models.CASCADE,to_field='id', related_name='chats')
  status = models.CharField(max_length=8,default=CHAT_STATUS.ACTIVE, choices=[
    (CHAT_STATUS.CREATE, 'CREATE'),
    (CHAT_STATUS.ACTIVE, 'ACTIVE'),
    (CHAT_STATUS.DISABLE, 'DISABLE'),
    (CHAT_STATUS.REMOVED, 'REMOVED'),
    (CHAT_STATUS.SOLVED, 'SOLVED'),
  ])
  REQUIRED_FIELDS = ['client','operator','status','company']
  
  def exist(**kwargs):
    try:
      chat = ChatWSP.objects.get(**kwargs)
      if chat:
        return True
    except ChatWSP.DoesNotExist:
      return False
    
  def check_get(self,client:ClientWSP):
    try:
      chat = ChatWSP.objects.get(client=client)
      if chat:
        return chat
      return None
    except ChatWSP.DoesNotExist:
      return None

class MessageWSP(models.Model):
  chat = models.ForeignKey(ChatWSP, on_delete=models.CASCADE, related_name="messages")
  msg = models.TextField()
  creation_on = models.DateTimeField(auto_now_add=True)
  destiny = models.CharField(max_length=10,default=MSG_DESTINATION.COMPANY, choices=[
    (MSG_DESTINATION.COMPANY, 'COMPANY'),
    (MSG_DESTINATION.CLIENT, 'CLIENT'),
  ])
  role = models.CharField(max_length=10, default=MSG_ROL.USER, choices=[
    (MSG_ROL.SYSTEM, 'SYSTEM'),
    (MSG_ROL.USER, 'USER'),
    (MSG_ROL.ASSISTANT, 'ASSISTANT'),
  ])
  REQUIRED_FIELDS = ['msg','destiny','chat','role']


class WSP():
  account_sid = os.environ.get('ACCOUNT_SID',default=env('ACCOUNT_SID'))
  auth_token = os.environ.get('AUTH_TOKEN',default=env('AUTH_TOKEN'))
  phone_number = os.environ.get('PHONE_NUMBER',default=env('PHONE_NUMBER'))
  def __init__(self):
    self.twilio_client = Client(self.account_sid,self.auth_token)
    
  def send_message(self, message:MessageWSP):
    client_phone= message.chat.client.phone_number
    company_phone= message.chat.company.phone
    if MSG_DESTINATION.CLIENT==message.destiny:
      send_to= client_phone
      send_by= company_phone
    else:
      send_to= company_phone 
      send_by= client_phone
    print('From_ whatsapp:'+send_by)
    print('To_whatsapp:'+send_to)
    print('Message: '+message.msg)
    message = self.twilio_client.messages.create(
      from_='whatsapp:'+send_by, 
      body=message.msg,
      to='whatsapp:'+send_to
    )
    return message
