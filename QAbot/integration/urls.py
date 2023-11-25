from django.urls import path

from integration.views import AnsweringBotAPIView

urlpatterns = [
    path("/answering-bot/", AnsweringBotAPIView.as_view(), name="answering_bot"),
]
