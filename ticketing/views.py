from genericpath import exists
from django.http import HttpResponse
from  rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView
from ticketing.serializers import QuestionTicketSerializer,AnswerTicketSerializer
# Create your views here.
from rest_framework import response,status
from rest_framework.permissions import IsAuthenticated
from ticketing.models import Ticket,TicketAnswer
from ticketing import docs ,params
from drf_yasg.utils import swagger_auto_schema


class CreateQuestionView(ListCreateAPIView):
    permission_classes =[IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = QuestionTicketSerializer
    def get_queryset(self):
        user = self.request.user
        type_ = self.request.GET.get('type')
        date_sort = self.request.GET.get('date')
        if user.type == '1':
            customer_id = self.request.GET.get('customer')
            if customer_id == None :
                queryset= Ticket.objects.all()
            else:
                queryset= Ticket.objects.filter(auther = customer_id)
        elif user.id is not exists:
            queryset= Ticket.objects.filter(auther=user.id)
        else:
            # return response.Response({'detail':'you cant'},status=status.HTTP_403_FORBIDDEN)
               return Ticket.objects.none()
            
        if type_ is not None:
            queryset = queryset.filter(type= type_)
        if date_sort is not None:
            queryset = queryset.order_by('-date')  # use -data ASC and data DESC
            
        return queryset
    @swagger_auto_schema(operation_description=docs.question_list_get,tags=['ticketing'],
                         manual_parameters=[params.date,params.customer,params.type])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.question_list_post,tags=['ticketing'])   
    def post(self, request, *args, **kwargs):
        if self.request.user:
            return self.create(request, *args, **kwargs)
        else:
            return response.Response({'detail':'you cant'},status=status.HTTP_403_FORBIDDEN)
    
    def perform_create(self, serializer):
        serializer.save(auther = self.request.user)

    
class CraetaAnswerView(ListCreateAPIView):
    permission_classes =[IsAuthenticated]
    queryset = TicketAnswer.objects.all()
    serializer_class = AnswerTicketSerializer
    def get_queryset(self):
        user = self.request.user
        question_id = self.request.GET.get('question')
        date_sort = self.request.GET.get('date')
        if user.type == '1':
            if question_id == None :
                queryset= TicketAnswer.objects.all()
            else:

                queryset= TicketAnswer.objects.filter(question = question_id)
        else:
           question_request =Ticket.objects.get(id = question_id) 

           if question_request.auther ==  self.request.user:
                queryset= TicketAnswer.objects.filter(question = question_id)
           else:
               return TicketAnswer.objects.none()
            
        if date_sort is not None:
            queryset = queryset.order_by('-date')  # use -data ASC and data DESC
        
        return queryset
    @swagger_auto_schema(operation_description=docs.answer_list_get,tags=['ticketing'],manual_parameters =[params.date,params.question])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.answer_list_post,tags=['ticketing'])
    def post(self, request, *args, **kwargs):
        question_id = self.request.data.get("question")
        question_request =Ticket.objects.get(id =question_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if question_request.auther ==  self.request.user or self.request.user.type == '1':
            self.perform_create(serializer,question_request)
            headers = self.get_success_headers(serializer.data)
            return response.Response(serializer.data, status=200, headers=headers)
        else:
            return response.Response({'detail':'you cant answer this question'},status=status.HTTP_403_FORBIDDEN)
        
    def perform_create(self, serializer,question_request):
        serializer.save(question = question_request,auther = self.request.user)

#####################update_delete##########################
class UpdateTicktetView(RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = QuestionTicketSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if self.request.user.id == serializer.data['auther'] or self.request.user.type == '1':
            return response.Response(serializer.data)
        else:
            return response.Response({'detail':'you cant show this question'},status=status.HTTP_403_FORBIDDEN)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # serializer.data['auther'] = instance.auther.id
        # print(serializer.data)
        if self.request.user == instance.auther:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return response.Response(serializer.data)
        else:
            return response.Response({'detail':'you cant show this question'},status=status.HTTP_403_FORBIDDEN)
    def perform_update(self, serializer):
        serializer.save(auther = self.request.user)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.request.user.id == instance.auther.id or self.request.user.type == '1':
            self.perform_destroy(instance)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return response.Response({'detail':'you cant show this question'},status=status.HTTP_403_FORBIDDEN)
        
    @swagger_auto_schema(operation_description=docs.question_update_retrieve,tags=['ticket'])   
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.question_update_update,tags=['ticket'])   
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.question_update_destroy,tags=['ticket'])   
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class UpdateTicktetAnswerView(RetrieveUpdateDestroyAPIView):
    queryset = TicketAnswer.objects.all()
    serializer_class = AnswerTicketSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(instance.auther)
        if self.request.user.id == serializer.data['auther'] or self.request.user.type == '1':
            return response.Response(serializer.data)
        else:
            return response.Response({'detail':'you cant show this question'},status=status.HTTP_403_FORBIDDEN)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # serializer.data['auther'] = instance.auther.id
        # print(serializer.data)
        print(instance)
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
        serializer.save(question = instance.question,auther = self.request.user)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.request.user.id == instance.auther.id or self.request.user.type == '1':
            self.perform_destroy(instance)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return response.Response({'detail':'you cant delete this answer'},status=status.HTTP_403_FORBIDDEN)
        
    @swagger_auto_schema(operation_description=docs.answer_update_retrieve,tags=['ticket'])   
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.answer_update_update,tags=['ticket'])   
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    @swagger_auto_schema(operation_description=docs.answer_update_destroy,tags=['ticket'])   
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)