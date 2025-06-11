from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import EntradaChatSerializer, ConversacionAnalizadaSerializer, SugerenciaRecepcionistaSerializer
from .models import ConversacionAnalizada
from .services.servicio_gemini import analizar_conversacion_con_gemini, sugerir_acciones_recepcionista_multiples


# Create your views here.
class AnalizarChatView(APIView):
    def post(self, request):
        serializer = EntradaChatSerializer(data=request.data)
        if serializer.is_valid():
            mensajes = serializer.validated_data['mensajes']
            id_context = serializer.validated_data.get('id_context')
            try:
                resultado = analizar_conversacion_con_gemini(mensajes)
            except Exception as e:
                return Response({"error": str(e)}, status=500)
            conversacion = ConversacionAnalizada.objects.create(
                id_context=id_context,
                mensajes=mensajes,
                sentimiento=resultado.get("sentimiento", "Neutral"),
                intencion_compra=resultado.get("intencion_compra", "Media"),
                urgencia=resultado.get("urgencia", "Media")
            )
            salida_serializer = ConversacionAnalizadaSerializer(conversacion)
            return Response(salida_serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ObtenerConversacionView(APIView):
    def get(self, request, id_context):
        try:
            conversaciones = ConversacionAnalizada.objects.filter(id_context=id_context).order_by('-creado_en')
            if not conversaciones.exists():
                return Response(
                    {"error": f"No se encontraron conversaciones con id_context: {id_context}"}, 
                    status=404
                )
            serializer = ConversacionAnalizadaSerializer(conversaciones, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
            return Response(
                {"error": f"No se encontró conversación con id_context: {id_context}"},
                status=404
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class SugerirAccionesRecepcionistaView(APIView):
    def post(self, request):
        serializer = SugerenciaRecepcionistaSerializer(data=request.data)
        if serializer.is_valid():
            conversaciones = serializer.validated_data['conversaciones']
            
            try:
                resultado = sugerir_acciones_recepcionista_multiples(conversaciones)
                return Response(resultado, status=200)
            except Exception as e:
                return Response({"error": str(e)}, status=500)
        return Response(serializer.errors, status=400)


class SugerirAccionesPorContextoView(APIView):
    def get(self, request, id_context):
        try:
            # Obtener todas las conversaciones para este id_context
            conversaciones = ConversacionAnalizada.objects.filter(id_context=id_context).order_by('-creado_en')
            if not conversaciones.exists():
                return Response(
                    {"error": f"No se encontraron conversaciones con id_context: {id_context}"}, 
                    status=404
                )
            
            # Serializar las conversaciones para pasarlas al servicio
            conversaciones_data = ConversacionAnalizadaSerializer(conversaciones, many=True).data
            
            # Generar sugerencias basadas en todas las conversaciones
            resultado = sugerir_acciones_recepcionista_multiples(conversaciones_data)
            return Response(resultado, status=200)
            
        except Exception as e:
            return Response({"error": str(e)}, status=500)