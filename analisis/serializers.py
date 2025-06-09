from rest_framework import serializers
from .models import ConversacionAnalizada

class EntradaChatSerializer(serializers.Serializer):
    id_context = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    mensajes = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )

class ConversacionAnalizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversacionAnalizada
        fields = '__all__'