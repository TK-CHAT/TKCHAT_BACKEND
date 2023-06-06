from django.db import models
from apps.users.models import User
from apps.companies.models import Company
from common.constants.constants import CHAT_STATUS,MSG_DESTINATION
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
  REQUIRED_FIELDS = ['client','operator','status']
  

class MessageWSP(models.Model):
  chat = models.ForeignKey(ChatWSP, on_delete=models.CASCADE)
  msg = models.TextField()
  creation_on = models.DateTimeField(auto_now_add=True)
  destiny = models.CharField(max_length=10,default=MSG_DESTINATION.COMPANY, choices=[
    (MSG_DESTINATION.COMPANY, 'COMPANY'),
    (MSG_DESTINATION.CLIENT, 'CLIENT'),
  ])
  REQUIRED_FIELDS = ['msg','destiny','chat']


class WSP():
  account_sid = os.environ.get('ACCOUNT_SID',default=env('ACCOUNT_SID'))
  auth_token = os.environ.get('AUTH_TOKEN',default=env('AUTH_TOKEN'))
  phone_number = os.environ.get('PHONE_NUMBER',default=env('PHONE_NUMBER'))
  def __init__(self):
    self.twilio_client = Client(self.account_sid,self.auth_token)
    
  def send_message(self, message:MessageWSP):
    print('From_ whatsapp:'+self.phone_number)
    print('To_whatsapp:'+message.send_to.phone_number)
    print('Message: '+message.msg)
    
    message = self.twilio_client.messages.create(
      from_='whatsapp:'+self.phone_number, 
      body=message.msg,
      to='whatsapp:'+message.chat.client.phone_number
    )
    print(dir(message))
    return message
