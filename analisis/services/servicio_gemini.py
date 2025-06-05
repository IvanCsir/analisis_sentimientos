import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY:", GEMINI_API_KEY)  # Para depuración, eliminar en producción
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def analizar_conversacion_con_gemini(mensajes):
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY no está configurada")

    # Unimos los mensajes para dar contexto a la IA
    historial = ""
    for i, m in enumerate(mensajes, 1):
        historial += f"Mensaje {i}: {m}\n"

    prompt = (
        "Analiza la siguiente conversación entre un cliente y un agente de un CRM hotelero. "
        "Responde SOLO en formato JSON con estos campos:\n"
        "sentimiento: (Positivo, Negativo o Neutral)\n"
        "intencion_compra: (Alta, Media o Baja)\n"
        "Ejemplo de respuesta:\n"
        "{ \"sentimiento\": \"Positivo\", \"intencion_compra\": \"Alta\" }\n\n"
        f"CONVERSACIÓN:\n{historial}"
    )

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

    import json
    try:
        resultado = json.loads(contenido)
    except Exception:
        resultado = {"sentimiento": "Neutral", "intencion_compra": "Media"}
    return resultado