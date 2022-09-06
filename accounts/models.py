from django.db import models

# Create your models here.
# Create your models here.
from django.contrib.auth.models import AbstractUser
Choices =(
    ('1','admin'),
    ('2','customer')
)
class CustomerUser(AbstractUser):
    type = models.CharField( max_length=5,choices=Choices,default='2')