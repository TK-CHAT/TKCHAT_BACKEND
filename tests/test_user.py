import pytest 
from apps.users.models import User

# Test create super User 
@pytest.mark.django_db
def test_superuser_creation():
  user = User.objects.create_superuser(
    first_name = 'Pedro',
    last_name= 'Garcia',
    email='pedro_garcia@gmail.com',
    password='fknakn1oid1d@-osdjk',
    date_of_birth='2000-05-08'
  )
  
  assert user.first_name=='prueba1'

# Test create User 
@pytest.mark.django_db
def test_superuser_creation():
  user = User.objects.create_user(
    first_name = 'Juan',
    last_name= 'Ramirez',
    email='juan_pr@gmail.com',
    password='fwinmkpsnnqnm1= dcs',
    date_of_birth='2000-05-08'
  )
  
  assert user.first_name=='prueba2'