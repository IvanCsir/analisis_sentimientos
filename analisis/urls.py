from django.urls import path
from .views import AnalizarChatView, ObtenerConversacionView, SugerirAccionesRecepcionistaView, SugerirAccionesPorContextoView

urlpatterns = [
    path('analizar_chat/', AnalizarChatView.as_view(), name='analizar_chat'),
    path('conversacion/<str:id_context>/', ObtenerConversacionView.as_view(), name='obtener_conversacion'),
    path('sugerir_acciones/', SugerirAccionesRecepcionistaView.as_view(), name='sugerir_acciones'),
    path('sugerir_acciones/<str:id_context>/', SugerirAccionesPorContextoView.as_view(), name='sugerir_acciones_por_contexto'),
]