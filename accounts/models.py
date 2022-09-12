from statistics import mode
from django.db import models

# Create your models here.
# Create your models here.
from django.contrib.auth.models import AbstractUser

from ticket_config.settings import AUTH_USER_MODEL
Choices =(
    ('1','admin'),
    ('2','customer')
)
class User(AbstractUser):
    type = models.CharField( max_length=5,choices=Choices,default='1')
    

class profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        abstract = True

class Customer(profile):
    phone = models.CharField(max_length=11)
    def __str__(self) -> str:
        return self.phone
    
class Admin(profile):
    phone = models.CharField(max_length=11)
    def __str__(self) -> str:
        return self.phone


    