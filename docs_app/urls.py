from django.urls import path
from docs_app.views import AnswerQuestion

urlpatterns = [
    path('answer/', AnswerQuestion.as_view(), name='answer_question'),
]