from rest_framework import serializers
from .models import ConversacionAnalizada

class EntradaChatSerializer(serializers.Serializer):
    mensajes = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )

class ConversacionAnalizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversacionAnalizada
        fields = '__all__'