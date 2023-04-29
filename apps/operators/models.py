from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Permission (models.Model):
  level = models.PositiveSmallIntegerField()
  description = models.CharField(max_length=120)


class Operator (models.Model):
  user = models.ManyToManyField(User)
  permission = models.OneToOneField(Permission, on_delete=models.SET_NULL,null=True)


