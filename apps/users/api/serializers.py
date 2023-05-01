from rest_framework import serializers
from apps.users.models import User


class AccountRegistrationSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)
   
  class Meta:
    model= User
    fields = ['email', 'date_of_birth', 'password', 'password2']
    extra_kwargs = {
      '[password]': {'write_only':True}
    }
  
  def save(self):
    user = User(
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
    check_email = User.objects.filter(email=value)
    if check_email is None:
      raise serializers.ValidationError({'email':'Does not match'})
    return value
  
  def validate_password(self,value):
    check_password = User.objects.filter(password=value)
    if check_password is None:
      raise serializers.ValidationError({'password':'Does not match'})
    return value
    
  