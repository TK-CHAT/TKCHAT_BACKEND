from django.db import models
import openai;
import os
# Create your models here.
import environ
env = environ.Env()

class openAI():
  _org_id=os.environ.get('OPENIA_ORG',default=env('OPENIA_ORG'))
  _api_key=os.environ.get('OPENIA_KEY',default=env('OPENIA_KEY'))
  def __init__(self):
    openai.organization = self._org_id
    openai.api_key= self._api_key
    self.__list_models= openai.Model.list()
    self.response = openai.ChatCompletion.create(
      model ="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
      ]
    )
    print(self.response)
    print(self.__list_models)
  
  def get_list_models(self):
    self.__list_models
  
  def get_response_by_message(msg:str):
    pass
    # return openai.Completion