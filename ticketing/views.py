# restframework import 
from  rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView
from rest_framework import response,status
from rest_framework.permissions import IsAuthenticated
# ticketing app import
from ticketing.serializers import QuestionTicketSerializer,AnswerTicketSerializer
from ticketing.permissions import Ticketpermissions
from ticketing.models import Ticket,TicketAnswer
from ticketing import docs ,params
# account app import
from accounts.models import Customer

# drf-ysg for swagger import
from drf_yasg.utils import swagger_auto_schema
# other app import
from datetime import date
# create view here
class CreateQuestionView(ListCreateAPIView):
    permission_classes =[IsAuthenticated,Ticketpermissions]
    serializer_class = QuestionTicketSerializer
    def get_queryset(self):
        user = self.request.user
        type_ = self.request.GET.get('type')
        datefirst = self.request.GET.get('datefirst')
        dateend = self.request.GET.get('dateend')
        if user.type == '1':
            customer_id = self.request.GET.get('customer')
            if customer_id == None :
                queryset= Ticket.objects.all()
            else:
                queryset= Ticket.objects.filter(auther__user_id = customer_id)
        else:
            queryset= Ticket.objects.filter(auther__user_id=user.id)
            # return response.Response({'detail':'you cant'},status=status.HTTP_403_FORBIDDEN)            
        if type_ is not None:
            queryset = queryset.filter(type= type_)
        if datefirst is not None and dateend is not None:
            # queryset = queryset.order_by('-date')  # use -data ASC and data DESC
            queryset=queryset.filter(date__gte=date.fromisoformat(datefirst),date__lte =dateend)
        elif  datefirst is not None:
            queryset=queryset.filter(date__gte=date.fromisoformat(datefirst))
        elif  dateend is not None:
            queryset=queryset.filter(date__lte =date.fromisoformat(dateend))
        return queryset
    @swagger_auto_schema(operation_description=docs.question_list_get,tags=['ticketing'],
                         manual_parameters=[params.date,params.customer,params.type])
    def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description=docs.question_list_post,tags=['ticketing'])   
    def post(self, request, *args, **kwargs):
                return self.create(request, *args, **kwargs)
            
    
    def perform_create(self, serializer):
        customer = Customer.objects.get(user_id = self.request.user.id)
        serializer.save(auther_id = customer.id)

     
class CraetaAnswerView(ListCreateAPIView):
    permission_classes =[IsAuthenticated]
    serializer_class = AnswerTicketSerializer
    def get_queryset(self):
        user = self.request.user
        ticket_id = self.kwargs['ticket_id']
        datefirst = self.request.GET.get('datefirst')
        dateend = self.request.GET.get('dateend')

        if user.type == '1':
            queryset= TicketAnswer.objects.filter(question_id = ticket_id)
        else:
            try:
                ticket_obj = Ticket.objects.get(id=ticket_id)
            except Ticket.DoesNotExist:
                return TicketAnswer.objects.none()
            
            if ticket_obj.auther.user ==  self.request.user:
                queryset= TicketAnswer.objects.filter(question_id = ticket_id)
            else:
                queryset = TicketAnswer.objects.none()
            
        if datefirst is not None and dateend is not None:
            # queryset = queryset.order_by('-date')  # use -data ASC and data DESC
            queryset=queryset.filter(date__gte=date.fromisoformat(datefirst),date__lte =dateend)
        elif  datefirst is not None:
            queryset=queryset.filter(date__gte=date.fromisoformat(datefirst))
        elif  dateend is not None:
            queryset=queryset.filter(date__lte =date.fromisoformat(dateend))                        
        return queryset
    @swagger_auto_schema(operation_description=docs.answer_list_get,tags=['ticketing'],manual_parameters =[params.date,params.question])
    def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.answer_list_post,tags=['ticketing'])
    def post(self, request, *args, **kwargs):
        
            ticket_id = self.kwargs['ticket_id']
            try:
                question = Ticket.objects.get(id =ticket_id)
            except Ticket.DoesNotExist:
                return response.Response({'detail':'does not exsit this id'},status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if question.auther.user ==  self.request.user or self.request.user.type == '1':
                self.perform_create(serializer,question)
                headers = self.get_success_headers(serializer.data)
                return response.Response(serializer.data, status=200, headers=headers)
            else:
                return response.Response({'detail':'you cant answer this ticket'},status=status.HTTP_400_BAD_REQUEST)


        
    def perform_create(self, serializer,question):
        serializer.save(question = question,auther = self.request.user)

#####################update_delete##########################
class UpdateTicktetView(RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAuthenticated]
    serializer_class = QuestionTicketSerializer
    def get_queryset(self):
        if  self.request.user.type == '1':
            queryset = Ticket.objects.all()
        else:
            queryset= Ticket.objects.filter(auther__user_id =self.request.user.id )
            # return response.Response({'detail':'you cant'},status=status.HTTP_403_FORBIDDEN)            
        return queryset
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if self.request.user == instance.auther.user:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return response.Response(serializer.data)
        else:
            return response.Response({'detail':'you cant update this question'},status=status.HTTP_403_FORBIDDEN)
    def perform_update(self, serializer):
        serializer.save(auther__user_id = self.request.user.id)
        
        
    @swagger_auto_schema(operation_description=docs.question_update_retrieve,tags=['ticketing'])   
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.question_update_update,tags=['ticketing'])   
    def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.question_update_destroy,tags=['ticketing'])   
    def delete(self, request, *args, **kwargs):
            return self.destroy(request, *args, **kwargs)

            
class UpdateTicktetAnswerView(RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAuthenticated]
    serializer_class = AnswerTicketSerializer
    def get_queryset(self):
        if  self.request.user.type == '1':
            queryset = TicketAnswer.objects.all()
        else:
            queryset= TicketAnswer.objects.filter(auther_id =self.request.user.id )
        return queryset

        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # serializer.data['auther'] = instance.auther.id
        # print(serializer.data)
        if self.request.user == instance.auther:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer,instance)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            
            return response.Response(serializer.data)
        else:
            return response.Response({'detail':'you cant change this answer'},status=status.HTTP_403_FORBIDDEN)
    def perform_update(self, serializer,instance):
        serializer.save(question_id = instance.question.id,auther = self.request.user)
                
    @swagger_auto_schema(operation_description=docs.answer_update_retrieve,tags=['ticketing'])   
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.answer_update_update,tags=['ticketing'])   
    def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.answer_update_destroy,tags=['ticketing'])   
    def delete(self, request, *args, **kwargs):
            return self.destroy(request, *args, **kwargs)
