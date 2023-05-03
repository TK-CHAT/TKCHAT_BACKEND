from rest_framework import serializers
from apps.companies.models import Company
from apps.users.models import User

class CompanySerializer(serializers.ModelSerializer):
  class Meta:
    model = Company
    fields = '__all__'
    lookup_field = 'user'
    
class CompanyRegistrationSerializer(serializers.ModelSerializer):
  name = serializers.CharField()
  class Meta:
    model= Company
    fields = ['name', 'email', 'phone']
  
  # def get_user_owner(self):
  #   ower_id = User.objects.parse_request_to_user_id(self.context)
  #   user_owner = User.objects.filter(id = ower_id)[0]
  #   if not user_owner.is_business_owner:
  #     raise serializers.ValidationError({'Error in token': 'the account does not have the privileges to create a company'})
  #   return user_owner
  
  def save(self,user):
    company = Company.objects.create(
      name = self.validated_data['name'],
      email = self.validated_data['email'],
      phone = self.validated_data['phone'],
      user = user
    )
    company.save()
    return company
  
