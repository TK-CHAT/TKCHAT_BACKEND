from rest_framework import serializers
from apps.operators.models import Operator
from apps.users.models import User
from apps.companies.models import Company

class OperatorRegistrationSerializer(serializers.ModelSerializer):
  class Meta:
    model= Operator
    fields = ['first_name','last_name','email','phone', 'work_company','date_of_birth', 'password']
    extra_kwargs = {
      '[password]': {'write_only': True}
    }
  
  def save(self):
    operator = Operator(
      first_name= self.validated_data['first_name'],
      last_name= self.validated_data['last_name'],
      email=self.validated_data['email'], 
      phone=self.validated_data['phone'], 
      date_of_birth=self.validated_data['date_of_birth'],
      work_company=self.validated_data['work_company'],
    )
    password = self.validated_data['password']
    operator.set_password(password)
    operator.is_admin = False
    operator.save()
    return operator
  