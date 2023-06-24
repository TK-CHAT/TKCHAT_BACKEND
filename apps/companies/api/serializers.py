from rest_framework import serializers
from apps.companies.models import Company
from apps.users.models import User

"""
  Default company data serializer
"""
class CompanySerializer(serializers.ModelSerializer):
  class Meta:
    model = Company
    fields= ['name','phone', 'email', 'user']
    extra_kwargs = {
      'user':{'required':True}
    }
  
  def validate_user(self, value):
    try:
      user = User.objects.get(email=value)
      if not user.is_admin:
        raise serializers.ValidationError('El usuario no tiene privilegios para crear empresas')
    except ValueError as e:
      raise serializers.ValidationError(e.args)
    return value

"""
  Default company data serializer, exclude user field
"""
class CompanyUpdateDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = Company
    fields= '__all__'
    extra_kwargs = {
      'user':{'required':True, }
    }
  
  def validate_user(self, value):
    try:
      user = User.objects.get(email=value)
      if not user.is_admin:
        raise serializers.ValidationError('El usuario no tiene privilegios para modificar datos de la empresa')
      if not self.context.user_id==user.id:
        raise serializers.ValidationError('El usuario no es el dueño de la empresa')
    except ValueError as e:
      raise serializers.ValidationError(e.args)
    return value
    
class ValidCompanySerializer(serializers.Serializer):
  id = serializers.IntegerField(required = True)
  
  def validate_id(self,value):
    try:
      company = Company.objects.filter(id=value)
      if len(company) == 0:
        raise serializers.ValidationError('El id de la empresa no está registrado')
    except ValueError as e:
      raise serializers.ValidationError(e.args)
        
    return value