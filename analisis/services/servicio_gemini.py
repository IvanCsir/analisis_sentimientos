import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def analizar_conversacion_con_gemini(mensajes):
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY no está configurada")

    # Unimos los mensajes para dar contexto a la IA
    historial = ""
    for i, m in enumerate(mensajes, 1):
        historial += f"Mensaje {i}: {m}\n"


    prompt = ("""
            # Rol
        Actuás como un analista experto en inteligencia artificial especializado en conversaciones del sector hotelero. Estás entrenado para evaluar múltiples mensajes escritos por un cliente durante un chat con el hotel y determinar, con claridad, el sentimiento general, la intención de compra y el nivel de urgencia, usando criterios específicos y objetivos.

        # Tarea
        Recibirás una secuencia de mensajes escritos por un cliente (excluyendo los del hotel). Tu tarea es analizar todos esos mensajes y clasificar el comportamiento del cliente en tres categorías con base en las siguientes definiciones:

        - **Sentimiento general** (evaluar el tono emocional general de los mensajes del cliente):
        - **Contento**: Usa lenguaje cordial, muestra entusiasmo, agradecimiento o buena predisposición.
        - **Enojado**: Muestra frustración, enojo, queja o descontento.
        - **Neutro**: Lenguaje objetivo o factual, sin carga emocional clara.

        - **Intención de compra** (evaluar si el cliente quiere hacer una reserva):
        - **Alta**: El cliente expresa intención directa de reservar o pide precio/disponibilidad con fechas concretas.
        - **Media**: El cliente hace consultas generales, menciona interés pero sin definir acciones concretas.
        - **Baja**: No hay señales de interés real en reservar (por ejemplo, solo hace una queja, saludo o duda general).

        - **Urgencia** (evaluar si el cliente necesita una respuesta rápida):
        - **Alta**: Usa lenguaje como “urgente”, “por favor respondan pronto”, “es para hoy”, o pregunta por disponibilidad inmediata.
        - **Media**: Pide respuesta pronta pero sin presión explícita.
        - **Baja**: No expresa necesidad de inmediatez ni indica un plazo.

        # Detalles Específicos
        - Evaluá el contenido completo de los mensajes del cliente como una unidad de análisis.
        - No tengas miedo de tomar decisiones firmes: si hay señales claras, asumí la categoría correspondiente.
        - Respondé solamente en formato JSON estructurado.
        - Si no hay suficiente información para una categoría, usá “indeterminado”.
        - No respondas con explicaciones ni reformulaciones, solo el JSON.

        # Contexto
        Este análisis se usará dentro de un CRM hotelero para priorizar la atención y detectar oportunidades de venta. El sistema automatizado depende de clasificaciones claras para funcionar correctamente.

        # Ejemplo
        ### Conversación del cliente:
        - “Hola, ¿tienen una habitación doble disponible para este fin de semana?”
        - “Sería para el viernes 12 al domingo 14. Me interesa si hay vista al mar.”
        - “Gracias, espero respuesta pronto porque quiero confirmar hoy mismo.”

        ### Respuesta esperada:
        ```json
        {
        "sentimiento": "Positivo",
        "intencion_compra": "Alta",
        "urgencia": "Alta"
        }
        ```

        # Conversación a analizar:
        """ + f"\n{historial}"
    )
    print("Historial de mensajes:", historial)
    print("Prompt completo:", prompt)
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    params = {"key": GEMINI_API_KEY}
    respuesta = requests.post(GEMINI_API_URL, params=params, json=data, timeout=20)
    respuesta.raise_for_status()
    contenido = respuesta.json()["candidates"][0]["content"]["parts"][0]["text"]
    
    print("Respuesta cruda de Gemini:", contenido)
    
    # Limpiar contenido de markdown si existe
    if "```json" in contenido:
        contenido = contenido.split("```json")[1].split("```")[0].strip()
    elif "```" in contenido:
        contenido = contenido.split("```")[1].split("```")[0].strip()
    
    print("Contenido limpio para parsear:", contenido)

    import json
    try:
        resultado = json.loads(contenido)
        print("JSON parseado exitosamente:", resultado)
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        print(f"Contenido que falló: {contenido}")
        resultado = {"sentimiento": "Neutral", "intencion_compra": "Media", "urgencia": "Media"}
    except Exception as e:
        print(f"Error inesperado: {e}")
        resultado = {"sentimiento": "Neutral", "intencion_compra": "Media", "urgencia": "Media"}
    return resultado