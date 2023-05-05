from rest_framework import serializers
from apps.companies.models import Company
from apps.users.models import User

"""
  Default company data serializer
"""
class CompanySerializer(serializers.ModelSerializer):
  class Meta:
    model = Company
    fields= '__all__'
  
  def valid_user(self, value):
    valid_user = User.objects.filter(id=value)
    if not valid_user.exists():
      raise serializers.ValidationError('No se pudo encontrar el usuario')
    return value

"""
  Default company data serializer, exclude user field
"""
class CompanyUpdateDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = Company
    fields= '__all__'
    read_only_fields = ('user','created_on')
  
  def valid_user(self, value):
    valid_user = User.objects.filter(id=value)
    if not valid_user.exists():
      raise serializers.ValidationError('No se pudo encontrar el usuario')
    if self.context['user']!= value:
      raise serializers.ValidationError('This user is not the company administrator')
    return value
  
    
 