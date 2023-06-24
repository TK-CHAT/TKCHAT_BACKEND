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
from common.constants.constants import MSG_ROL
import json

class Bot(User):
  _bot_mail="default@msg.bot"
  temperature = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(2.00)],default=1.00)
  company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='bot')
  REQUIRED_FIELDS = ['first_name','last_name','date_of_birth','temperature','company']
  
  def exist(self):
    try:
      bot = self.objects.get(email=self._bot_mail)
      if bot:
        return True
    except self.DoesNotExist:
      return False
    return False

  def get_register_query(self,company):
    password= generate_random_password(10)
    chat_query = {
      "email" : self._bot_mail,
      "date_of_birth": datetime.today().strftime('%Y-%m-%d'),
      "password":password,
      "first_name":"EGO",
      "last_name":"tkbot",
      "temperature":1.00,
      "company": company.id
    }
    return chat_query
  
  def get_user_bot(self,company):
    try:
      bot = Bot.objects.get(email=self._bot_mail, company=company)
      return bot
    except Bot.DoesNotExist:
      return None
  
  def get_query(self):
    prompts = self.prompts.all()
    prompts=list(prompts.values())
    query= {
      'id':self.id,
      'temperature':self.temperature,
      'company': self.company.id,
      'prompts': prompts
    }
    return query

class BotPrompts(models.Model):
  bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="prompts")
  prompt = models.TextField()
  role = models.CharField(max_length=10, choices=[
        (MSG_ROL.SYSTEM, 'SYSTEM'),
        (MSG_ROL.ASSISTANT, 'ASSISTANT'),
    ])
  
class openAI():
  _org_id=os.environ.get('OPENIA_ORG',default=env('OPENIA_ORG'))
  _api_key=os.environ.get('OPENIA_KEY',default=env('OPENIA_KEY'))
  def __init__(self):
    openai.organization = self._org_id
    openai.api_key= self._api_key
    self.__list_models= openai.Model.list()
  
  def get_list_models(self):
    self.__list_models
  
  def get_response_chat(self,chat:ChatWSP, bot:Bot):
    messages = chat.messages.all()
    bot_prompts = bot.prompts.all()
    chatGPT_msg= []
    for prompt in bot_prompts:
      chatGPT_msg.append({
        'role': prompt.role.lower(),
        'content': prompt.prompt
      })
    for message in messages:
      chatGPT_msg.append({
        'role': message.role.lower(),
        'content': message.msg
      })
    print(chatGPT_msg)
    response = openai.ChatCompletion.create(
      model ="gpt-3.5-turbo",
      messages=chatGPT_msg
    )
    return response
  
  def parse_chat_to_chatGTP_message(chat: ChatWSP):
    messages = []
    for message in chat.messages.all():
        messages.append({
            "content": message.msg
        })
    return messages
  
  def get_response_msg(self,message:str):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=message,
      max_tokens=50
    )
    data = json.loads(str(response))
    return data