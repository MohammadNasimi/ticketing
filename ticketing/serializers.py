from rest_framework import serializers
from ticketing.models import Ticket,TicketAnswer
from accounts.serializers import UserSerializer,Customerserilizer

class AnswerTicketSerializer(serializers.ModelSerializer):
    auther = UserSerializer(read_only=True)
    
    class Meta:
        fields = ['id','question','auther','text','date']
        model = TicketAnswer
        read_only_fields =['id','question','auther','date']
        
class QuestionTicketSerializer(serializers.ModelSerializer):
    auther = Customerserilizer(read_only=True)
    ticket_answer_obj = serializers.SerializerMethodField('get_ticket_answer_obj')

    class Meta:
        fields = ['id','title' , 'auther','text', 'date','type','ticket_answer_obj']
        model = Ticket
        read_only_fields =['id','auther','date','ticket_answer_obj']
        
    
    def get_ticket_answer_obj(self, obj):
        results = TicketAnswer.objects.filter(question = obj.id)
        return AnswerTicketSerializer(results, many=True).data