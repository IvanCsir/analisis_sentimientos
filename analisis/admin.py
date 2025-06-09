from django.contrib import admin
from .models import ConversacionAnalizada

# Register your models here.
@admin.register(ConversacionAnalizada)
class ConversacionAnalizadaAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_context','sentimiento', 'intencion_compra','urgencia', 'creado_en')
    search_fields = ('mensajes',)
    readonly_fields = ('creado_en',)