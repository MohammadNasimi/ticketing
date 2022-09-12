from operator import mod
from django.db import models
from accounts.models import Customer,User
# Create your models here.
Choices_type =(
    ( '1','Financial'),
    ('2','Social'),
    ('3','holiday'),
    ('4','Others')
)
class Ticket(models.Model):
    title = models.CharField(max_length=20)
    auther = models.ForeignKey(Customer,on_delete=models.CASCADE)
    text = models.TextField()
    date =models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=2,choices = Choices_type, default= '4')
    def __str__(self) -> str:
        return self.title
    


class TicketAnswer(models.Model):
    question = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    auther = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    date =models.DateTimeField(auto_now_add=True)

    
    def __str__(self) -> str:
        return self.question.title