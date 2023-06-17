from django.db import models
import openai;
from apps.users.models import User
from apps.companies.models import Company
import os
from datetime import datetime
from common.functions.functions import generate_random_password
from django.core.validators import MinValueValidator, MaxValueValidator
import environ
env = environ.Env()
import json
from apps.wsp.models import ChatWSP



class Bot(User):
  _bot_mail="default@msg.bot"
  temperature = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(2.00)],default=1.00)
  company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='bot')
  REQUIRED_FIELDS = ['first_name','last_name','date_of_birth','temperature','company']
  
  def exist(self):
    try:
      bot = self.objects.get(email=self.bot_mail)
      if bot:
        return True
    except self.DoesNotExist:
      return False
    return False

  def create(self,company):
    if self.exist():
      return False
    password= generate_random_password(10)
    try:
      self.objects.create(
        email = self.bot_mail,
        date_of_birth= datetime.now(),
        password=password,
        first_name="EGO",
        last_name="tkbot",
        temperature=1.00,
        company= company
      )
    except:
      return False
    return True
  
  def get_user_bot(self):
    try:
      bot = self.objects.get(email=self.bot_mail)
      return bot
    except self.DoesNotExist:
      return None



class openAI():
  _org_id=os.environ.get('OPENIA_ORG',default=env('OPENIA_ORG'))
  _api_key=os.environ.get('OPENIA_KEY',default=env('OPENIA_KEY'))
  def __init__(self):
    openai.organization = self._org_id
    openai.api_key= self._api_key
    self.__list_models= openai.Model.list()
  
  def get_list_models(self):
    self.__list_models
  
  def get_response_chat(chat:ChatWSP):
    
    response = openai.ChatCompletion.create(
      model ="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
      ]
    )
  
  def parse_chat_to_chatGTP_message(chat: ChatWSP):
    messages = []
    for message in chat.messages.all():
        messages.append({
            "content": message.msg
        })
    return messages
  
  def get_response_msg(message:str):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=message
    )
    data = json.loads(response)
    return data