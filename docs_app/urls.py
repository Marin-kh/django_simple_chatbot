from django.urls import path
from .views import AnswerQuestion, home

urlpatterns = [
    path('', home, name='home'),
    path('answer/', AnswerQuestion.as_view(), name='answer_question'),
]