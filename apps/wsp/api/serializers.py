from rest_framework import serializers
from apps.wsp.models import MessageWSP,ClientWSP,ChatWSP
from common.constants.constants import CHAT_STATUS
import re


class WPSMessageSerializer(serializers.ModelSerializer):
  class Meta:
    model= MessageWSP
    fields = ['msg','destiny','chat','role']
  

class ClientWPSSerializer(serializers.ModelSerializer):
  
  class Meta:
    model=ClientWSP
    fields = ['phone_number',]
    
  def validate_phone_number(self,value):
    pattern = re.compile(r'^\+\d+$')
    if pattern.match(value):
      return value 
    raise serializers.ValidationError('El número de telefono no es valido')

  def create(self, validated_data):
    phone_number = validated_data.get('phone_number')
    client, created = ClientWSP.objects.get_or_create(phone_number=phone_number)
    return client
  
class ChatWSPSerializer(serializers.ModelSerializer):
  class Meta:
    model=ChatWSP
    fields = ['client','operator','company']

  def save(self, **kwargs):
      self.validated_data['status'] = CHAT_STATUS.ACTIVE
      super().save(**kwargs)
      
class ChatWSPDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model=ChatWSP
    fields = '__all__'