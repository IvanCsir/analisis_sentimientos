from django.urls import path
from .views import AnalizarChatView

urlpatterns = [
    path('analizar_chat/', AnalizarChatView.as_view(), name='analizar_chat'),
]