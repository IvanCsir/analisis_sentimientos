from django.db import models

# Create your models here.

class ConversacionAnalizada(models.Model):
    mensajes = models.JSONField()
    sentimiento = models.CharField(max_length=12)  # Positivo, Negativo, Neutral
    intencion_compra = models.CharField(max_length=8)  # Alta, Media, Baja
    urgencia = models.CharField(max_length=8,default="Media")  # Alta, Media, Baja
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sentimiento: {self.sentimiento} | Intención: {self.intencion_compra} | Urgencia: {self.urgencia}"