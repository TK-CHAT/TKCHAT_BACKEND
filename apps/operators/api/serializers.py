from rest_framework import serializers
from apps.operators.models import Operator
from apps.users.models import User
from apps.companies.models import Company

class OperatorRegistrationSerializer(serializers.ModelSerializer):
  user = serializers.IntegerField(required=True, write_only=True)
  class Meta:
    model= Operator
    fields = ['first_name','last_name','email','phone', 'work_company','user','date_of_birth', 'password']
    extra_kwargs = {
      '[password]': {'write_only': True},
      'first_name': {'required':True},
      'last_name': {'required':True},
      'work_company': {'required':True},
    }
  
  def validate_work_company(self,value):
    try:
      company = Company.objects.get(name=str(value))
      if not company:
        raise serializers.ValidationError('La empresa no existe')   
    except ValueError as e:
      raise serializers.ValidationError(e.args)
    finally:
      return value
  
  def validate_user(self,value):
    try:
      company = Company.objects.get(id=self.context['work_company'])
      user = User.objects.get(id=value)
      if not user == company.user:
        raise serializers.ValidationError('El usuario no es administrador de la empresa')
      if not user.is_admin:
        raise serializers.ValidationError('El usuario no es administrador')
    except ValueError as e:
      raise serializers.ValidationError(e.args)
    finally:
      return value
      
  
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

class OperatorUpdateSerializer(serializers.ModelSerializer):
  user = serializers.IntegerField(required=True, write_only=True)
  class Meta:
    model=Operator
    fields='__all__'
    
  def validate_work_company(self,value):
    try:
      company = Company.objects.get(name=str(value))
      if not company:
        raise serializers.ValidationError('La empresa no existe')   
    except ValueError as e:
      raise serializers.ValidationError(e.args)
    finally:
      return value
  
  def validate_user(self,value):
    try:
      company = Company.objects.get(id=self.context['work_company'])
      user = User.objects.get(id=value)
      if not user == company.user:
        raise serializers.ValidationError('El usuario no es administrador de la empresa')
      if not user.is_admin:
        raise serializers.ValidationError('El usuario no es administrador')
    except ValueError as e:
      raise serializers.ValidationError(e.args)
    finally:
      return value


