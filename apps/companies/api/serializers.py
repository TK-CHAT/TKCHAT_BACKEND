from rest_framework import serializers
from apps.companies.models import Company
from apps.users.models import User

"""
  Default company data serializer, exclude user field
"""
class CompanyDataSerializer(serializers.ModelSerializer):
  user_id = serializers.CharField(required=True)
  class Meta:
    model = Company
    fields= '__all__'
    read_only_fields = ('user','user_id')
    
    
"""
  Custom company registration serializer with user_id 
"""
class CompanyRegistrationSerializer(serializers.ModelSerializer):
  user_id = serializers.CharField(required=True)
  class Meta:
    model= Company
    fields = ['name', 'email', 'phone', 'user_id']
  
  def validate_user_id(self,value):
    valid_user = User.objects.filter(id=value)
    if not valid_user.exists():
      raise serializers.ValidationError({'token':'User not found'})
    return value
  
  def save(self):
    user = User.objects.filter(id=self.validated_data['user_id'])[0]
    company = Company.objects.create(
      name = self.validated_data['name'],
      email = self.validated_data['email'],
      phone = self.validated_data['phone'],
      user = user
    )
    company.save()
    return company
