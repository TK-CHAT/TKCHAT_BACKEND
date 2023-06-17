from rest_framework import serializers
from apps.tkbot.models import Bot

class botSerializer(serializers.ModelSerializer):
  class Meta:
    model= Bot
    fields = '__all__'