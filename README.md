# analisis_sentimientos
Se propone desarrollar un microservicio de análisis de sentimientos que se integrará con nuestro CRM actual para mejorar la comprensión de las interacciones con los clientes. Utilizando inteligencia artificial, el servicio analizará la comunicación del cliente para determinar sentimientos, intención de compra y nivel de urgencia.

Documentación extensa: https://docs.google.com/document/d/1bZNSIPIf--G_ElG9ly_SOsuYQjLUbXM9wcckPLGvGJc/edit?usp=sharing

Cuatro endpoints importantes:


1. Análisis de Conversación
POST https://analisis-sentimientos-zsgq.onrender.com/api/analizar_chat/ →
Analiza los mensajes de un cliente y devuelve el análisis de sentimiento, intención de compra y urgencia.
	
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

GET https://analisis-sentimientos-zsgq.onrender.com/api/conversacion/{id_context}/ →
Devuelve el historial de análisis de una conversación, ordenado por fecha (más reciente primero).

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

3. Sugerencias para Recepcionista por array de conversaciones

POST /api/sugerir_acciones/
Envía uno o varios análisis de conversaciones para recibir una sugerencia de acción para el recepcionista.

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
        },

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
```

4. Sugerencias para Recepcionista by id_context
GET https://analisis-sentimientos-zsgq.onrender.com/api/sugerir_acciones/<id_context>/
Recibe sugerencias considerando el historial completo de ese contexto/conversación.

Respuesta:
```json
{
  "prioridad": "alta",
  "tono_sugerido": "empático",
  "accion_sugerida": "Confirmar disponibilidad inmediata para esta noche",
  "alerta": "Cliente urgente - responder inmediatamente"
}
```


D