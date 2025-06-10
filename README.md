# analisis_sentimientos
Se propone desarrollar un microservicio de análisis de sentimientos que se integrará con nuestro CRM actual para mejorar la comprensión de las interacciones con los clientes. Utilizando inteligencia artificial, el servicio analizará la comunicación del cliente para determinar sentimientos, intención de compra y nivel de urgencia. 

Tres endpoints importantes:

1. Análisis de Conversación
POST /api/analizar_chat/ →
Entrada
```json
{
    "id_context": "cliente_123",
    "mensajes": [
        "Hola, necesito una habitación urgente",
        "Es para esta noche, por favor confirmen pronto"
    ]
}
```

Respuesta:
```json
{
    "id": 1,
    "id_context": "cliente_123",
    "mensajes": ["Hola, necesito una habitación urgente", "Es para esta noche, por favor confirmen pronto"],
    "sentimiento": "Neutro",
    "intencion_compra": "Alta",
    "urgencia": "Alta",
    "creado_en": "2025-06-06T15:30:00Z"
}
```

2. Obtener Historial por Contexto/Conversación

GET /api/conversacion/{id_context}/ →

Respuesta:
```json
[
    {
        "id": 2,
        "id_context": "cliente_123",
        "mensajes": ["Mensaje más reciente"],
        "sentimiento": "Contento",
        "intencion_compra": "Alta",
        "urgencia": "Media",
        "creado_en": "2025-06-06T16:00:00Z"
    },
    {
        "id": 1,
        "id_context": "cliente_123", 
        "mensajes": ["Mensaje anterior"],
        "sentimiento": "Neutro",
        "intencion_compra": "Media",
        "urgencia": "Baja",
        "creado_en": "2025-06-06T15:30:00Z"
    }
]

3. Sugerencias para Recepcionista

POST /api/sugerir_acciones/

Entrada:
```json
{
    "conversaciones": [
        {
            "id": 1,
            "id_context": "cliente_123",
            "mensajes": ["Hola", "Necesito habitación urgente"],
            "sentimiento": "Neutro",
            "intencion_compra": "Alta",
            "urgencia": "Alta",
            "creado_en": "2025-06-06T15:30:00Z"
        }
    ]
}
```

Respuesta:
```json
{
    "prioridad": "alta",
    "tono_sugerido": "empático",
    "accion_sugerida": "Confirmar disponibilidad inmediata para esta noche",
    "alerta": "Cliente urgente - responder inmediatamente"
}
