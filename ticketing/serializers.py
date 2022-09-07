from rest_framework import serializers
from ticketing.models import Ticket,TicketAnswer
from accounts.serializers import UserSerializer
class QuestionTicketSerializer(serializers.ModelSerializer):
    auther = UserSerializer(read_only=True)

    class Meta:
        fields = ['id','title' , 'auther','text', 'date','type']
        model = Ticket
        read_only_fields =['id','auther','date']
class AnswerTicketSerializer(serializers.ModelSerializer):
    auther = UserSerializer(read_only=True)
    class Meta:
        fields = ['id','question','auther','text','date']
        model = TicketAnswer
        read_only_fields =['id','auther','date']