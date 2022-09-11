from django.urls import path,include
from ticketing.views import CreateQuestionView,CraetaAnswerView,UpdateTicktetView,UpdateTicktetAnswerView
urlpatterns = [
    path('ticket/list/',CreateQuestionView.as_view(),name = 'create_question'),
    path('ticketanswer/list/<int:pk>/',CraetaAnswerView.as_view(),name = 'create_answer'),
    path('ticket/detail/<int:pk>/',UpdateTicktetView.as_view(),name = 'detail_question'),
    path('ticketanswer/detail/<int:pk>/',UpdateTicktetAnswerView.as_view(),name = 'detail_Answer')
]