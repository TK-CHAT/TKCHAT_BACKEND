from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth import hashers
from apps.companies.models import Company
from apps.companies.api.serializers import CompanyUpdateDataSerializer

class UserDataSerializer(serializers.ModelSerializer):
  companies = CompanyUpdateDataSerializer(many=True, read_only=True)
  class Meta:
    model = User
    fields = ['id','email','date_of_birth','is_active','is_admin','companies']
    lookup_field = 'id'

"""
  Validate user_id from jtw token
"""
class UserIdSerializer(serializers.Serializer):
  user = serializers.IntegerField(required=True)
  
  def validate_user(self,value):
    valid_user = User.objects.filter(id=value)
    if not valid_user.exists():
      raise serializers.ValidationError({'token': 'User not found'})
    return value

class UserAdminRegistrationSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)
  class Meta:
    model= User
    fields = ['first_name','last_name','email', 'date_of_birth', 'password', 'password2']
    extra_kwargs = {
      '[password]': {'write_only':True}
    }
  
  def save(self):
    user = User(
      first_name= self.validated_data['first_name'],
      last_name= self.validated_data['last_name'],
      email=self.validated_data['email'], 
      date_of_birth=self.validated_data['date_of_birth']
    )
    password = self.validated_data['password']
    password2 = self.validated_data['password2']
    if password != password2:
      raise serializers.ValidationError({'password': 'Passwords must match.'})
    user.set_password(password)
    user.is_admin = True
    user.save()
    return user

class PasswordChangeSerializer(serializers.Serializer):
  current_password = serializers.CharField(style={"input_type": "password"}, required=True)
  new_password = serializers.CharField(style={"input_type": "password"}, required=True)

  def validate_current_password(self, value):
      if not self.context['request'].user.check_password(value):
          raise serializers.ValidationError({'current_password': 'Does not match'})
      return value

class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField(required=True)
  password = serializers.CharField(style={"inpuy_type": "password"},required=True)
  
  def validate_email(self,value):
    valid_user_list = User.objects.filter(email=value)
    if len(valid_user_list) == 0:
      raise serializers.ValidationError({'email':'Does not match'})
    valid_user = valid_user_list[0]
    if hashers.check_password(self.context['password'],valid_user.password) == False:
      raise serializers.ValidationError({'email':'Password  or email do not match'})
    return value
  
  def get_context_token(self):
    user = User.objects.filter(email= self.context['email'])[0]
    context_token = user.generate_context_token()
    return context_token
    
  
    
  