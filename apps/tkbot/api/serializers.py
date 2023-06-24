from rest_framework import serializers
from apps.tkbot.models import Bot,BotPrompts
from apps.users.models import User

class botSerializer(serializers.ModelSerializer):
  class Meta:
    model= Bot
    fields = '__all__'

class botPromptsSerializer(serializers.ModelSerializer):
  class Meta:
    model= BotPrompts
    fields = '__all__'
  
  def validate_bot(self,value):
    print(value)
    try: 
      bot = Bot.objects.get(id=value.id)
    except Bot.DoesNotExist:
      raise serializers.ValidationError('El bot no existe')
    user:User = self.context['user']
    companies_list = user.companies.all()
    if bot.company not in companies_list:
      raise serializers.ValidationError('El bot no pertence a la empresa')
    return value
  