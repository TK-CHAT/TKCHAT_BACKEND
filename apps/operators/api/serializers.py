from rest_framework import serializers
from apps.users.models import User

class OperatorRegistrationSerializer(serializers.ModelSerializer):
  class Meta: 
    model= User
    fields = ['email', 'date_of_birth', 'password']
    extra_kwargs = {
      '[password]': {'write_only': True}
    }
  def save(self):
    
    user = User(
      email=self.validated_data['email'], 
      date_of_birth=self.validated_data['date_of_birth']
    )
    password = self.validated_data['password']
    user.set_password(password)
    user.is_admin = False
    user.save()
    return user
    
  