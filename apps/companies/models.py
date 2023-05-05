from django.db import models
from apps.users.models import User

# Create your models here.
class Company(models.Model):
  name = models.CharField(max_length=255, unique=True)
  email = models.EmailField(max_length=255,unique=True)
  phone = models.CharField(max_length=15)
  created_on = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User,on_delete=models.CASCADE, to_field='id')
  
  REQUIRED_FIELDS = ['name','email','owner_id']
  
  def __str__(self):
    return self.name
  