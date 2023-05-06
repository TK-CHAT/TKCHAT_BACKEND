from django.db import models
from apps.users.models import User
from apps.companies.models import  Company

# Create your models here.

class Operator(User):
  work_company = models.ForeignKey(Company, on_delete=models.PROTECT,to_field='id', related_name='employees')
  user = models.ForeignKey(User, on_delete=models.PROTECT,to_field='id', related_name='operators')
  
  REQUIRED_FIELDS = ['first_name','last_name','email','phone','work_company','user']
  def __str__(self):
    return self.name
  