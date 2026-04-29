from django.urls import path
from .views import chat

urlpatterns = [
    path('chat_bot/', chat, name='chat_bot')
]


#este archivo es para la url de la api 