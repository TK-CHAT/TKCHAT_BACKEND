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
  class Meta:
    model=Operator
    fields=['first_name','last_name','email','phone','is_active','work_company','id','date_of_birth']
    extra_kwargs = {
      'work_company': {'read_only':True},
      'id': {'read_only':True},
    }
    

class OperatorIdValidatorSerializer(serializers.Serializer):
  id = serializers.IntegerField(required=True)
  user = serializers.IntegerField(required=True)
  work_company = serializers.IntegerField(required=True)
  
  def validate_id(self,value):
    try:
      Operator.objects.get(id=value)
    except Operator.DoesNotExist:
      raise serializers.ValidationError('El id operador no existe')
    return value
  
  def validate_user(self,value):
    try:
      User.objects.get(id=value)
    except User.DoesNotExist:
      raise serializers.ValidationError('El usuario token no existe')
    return value
      
    
  def validate_work_company(self,value):
    try:
      Company.objects.get(id=value)
    except Company.DoesNotExist:
      raise serializers.ValidationError('La compañia no existe')
    return value
  
  def validate(self, value):
    try:
      valid_operator = Operator.objects.get(id=value['id'])
      valid_company = Company.objects.get(id=value['work_company'])
      valid_user = User.objects.get(id = value['user'])
      if not valid_operator.work_company == valid_company:
        raise serializers.ValidationError('El operador no trabaja para la compañia ' + str(valid_company))
      if not valid_company.user == valid_user:
        raise serializers.ValidationError('El user token no es administrador de la compañia')
    except ValueError as e:
      raise serializers.ValidationError(e.args)
    return value