from django.urls import path,include
from ticketing.views import CreateQuestionView,CraetaAnswerView,UpdateTicktetView,UpdateTicktetAnswerView
urlpatterns = [
    path('Ticket/list/',CreateQuestionView.as_view(),name = 'create_question'),
    path('TicketAnswer/list/',CraetaAnswerView.as_view(),name = 'create_answer'),
    path('Ticket/detail/<int:pk>/',UpdateTicktetView.as_view(),name = 'detail_question'),
    path('TicketAnswer/detail/<int:pk>/',UpdateTicktetAnswerView.as_view(),name = 'detail_Answer')
]