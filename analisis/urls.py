from django.urls import path
from .views import AnalizarChatView, ObtenerConversacionView

urlpatterns = [
    path('analizar_chat/', AnalizarChatView.as_view(), name='analizar_chat'),
    path('conversacion/<str:id_context>/', ObtenerConversacionView.as_view(), name='obtener_conversacion'),
]