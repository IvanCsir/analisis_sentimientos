from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import EntradaChatSerializer, ConversacionAnalizadaSerializer
from .models import ConversacionAnalizada
from .services.servicio_gemini import analizar_conversacion_con_gemini


# Create your views here.
class AnalizarChatView(APIView):
    def post(self, request):
        serializer = EntradaChatSerializer(data=request.data)
        if serializer.is_valid():
            mensajes = serializer.validated_data['mensajes']
            try:
                resultado = analizar_conversacion_con_gemini(mensajes)
            except Exception as e:
                return Response({"error": str(e)}, status=500)
            conversacion = ConversacionAnalizada.objects.create(
                mensajes=mensajes,
                sentimiento=resultado.get("sentimiento", "Neutral"),
                intencion_compra=resultado.get("intencion_compra", "Media"),
            )
            salida_serializer = ConversacionAnalizadaSerializer(conversacion)
            return Response(salida_serializer.data, status=201)
        return Response(serializer.errors, status=400)