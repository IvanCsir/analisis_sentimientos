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
    #print("Prompt completo:", prompt)
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


def sugerir_acciones_recepcionista_multiples(conversaciones):
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY no está configurada")

    # Preparar análisis consolidado de múltiples conversaciones
    id_context = conversaciones[0].get('id_context', 'No especificado')
    analisis_consolidado = []
    todos_los_mensajes = []
    
    # Procesar cada conversación
    for i, conv in enumerate(conversaciones, 1):
        sentimiento = conv.get('sentimiento', 'Neutro')
        intencion = conv.get('intencion_compra', 'Media')
        urgencia = conv.get('urgencia', 'Media')
        mensajes = conv.get('mensajes', [])
        fecha = conv.get('creado_en', 'Sin fecha')
        
        analisis_consolidado.append(f"""
        Conversación {i} ({fecha}):
        - Sentimiento: {sentimiento}
        - Intención de compra: {intencion}
        - Urgencia: {urgencia}
        - Mensajes: {', '.join(mensajes)}
        """)
        
        # Agregar todos los mensajes a la lista consolidada
        todos_los_mensajes.extend(mensajes)
    
    # Determinar tendencias generales
    sentimientos = [conv.get('sentimiento', 'Neutro') for conv in conversaciones]
    intenciones = [conv.get('intencion_compra', 'Media') for conv in conversaciones]
    urgencias = [conv.get('urgencia', 'Media') for conv in conversaciones]
    
    # Obtener el análisis más reciente
    ultimo_sentimiento = conversaciones[0].get('sentimiento', 'Neutro')
    ultima_intencion = conversaciones[0].get('intencion_compra', 'Media')
    ultima_urgencia = conversaciones[0].get('urgencia', 'Media')

    prompt = f"""
    # Rol
    Eres un experto en atención al cliente hotelero y gestor de experiencias.
    Tu tarea es proporcionar solamente una SUGERENCIA específica y práctica para 
    que un recepcionista atienda de manera óptima a este cliente según su perfil emocional y
    comercial basado en MÚLTIPLES conversaciones. No debés entrar en reglas de negocio específicas del hotel.

    # Historial de conversaciones del cliente
    ID del contexto: {id_context}
    Número total de conversaciones: {len(conversaciones)}
    
    {chr(10).join(analisis_consolidado)}
    
    # Análisis más reciente (conversación principal)
    - **Sentimiento actual**: {ultimo_sentimiento}
    - **Intención de compra actual**: {ultima_intencion}
    - **Urgencia actual**: {ultima_urgencia}
    
    # Tendencias observadas
    - Sentimientos en el historial: {', '.join(sentimientos)}
    - Intenciones en el historial: {', '.join(intenciones)}
    - Urgencias en el historial: {', '.join(urgencias)}
    
    # Todos los mensajes del cliente (cronológico):
    {chr(10).join([f"{i+1}. {msg}" for i, msg in enumerate(todos_los_mensajes)])}

    # Tu tarea
    Basándote en el HISTORIAL COMPLETO y la conversación más reciente, proporciona sugerencias específicas y accionables para el recepcionista. 
    Ten en cuenta la evolución del cliente y su comportamiento histórico.

    # Consideraciones especiales para múltiples conversaciones:
    - Si hay conversaciones repetidas, el cliente podría estar comparando opciones
    - Si la urgencia aumentó, necesita atención prioritaria
    - Si la intención de compra es consistentemente alta, es un lead caliente
    - Si el sentimiento empeoró, hay que recuperar la confianza
    - Si es un cliente recurrente, personalizar la atención

    # Guías específicas:

    ## Por URGENCIA ACTUAL:
    **Alta**: Respuesta inmediata, facilitar proceso, confirmar disponibilidad al instante
    **Media**: Respuesta pronta pero con más detalles, ofrecer opciones
    **Baja**: Respuesta completa con información educativa

    ## Por INTENCIÓN DE COMPRA ACTUAL:
    **Alta**: Enfocar en cerrar venta, minimizar fricción, acelerar proceso de reserva
    **Media**: Nutrir con información valiosa, construir confianza, ofrecer opciones
    **Baja**: Educación sobre valor, crear interés, seguimiento de largo plazo

    ## Por SENTIMIENTO ACTUAL:
    **Contento**: Mantener buena energía, aprovechar momentum positivo
    **Enojado**: Empatía, resolución de problemas, gestos de buena voluntad
    **Neutro**: Crear conexión emocional

    # Formato de respuesta
    Responde en formato JSON con esta estructura exacta y CONCISA:
    {{
        "prioridad": "alta/media/baja",
        "tono_sugerido": "formal/amigable/empático",
        "accion_sugerida": "Una acción específica a realizar",
        "alerta": "Una alerta breve si es necesaria o null"
    }}

    #Instrucción crítica:
    No entrar en reglas de negocio debido a que no conoces el contexto de los hoteles.
        """

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
    respuesta = requests.post(GEMINI_API_URL, params=params, json=data, timeout=30)
    respuesta.raise_for_status()
    contenido = respuesta.json()["candidates"][0]["content"]["parts"][0]["text"]
    
    print("Respuesta cruda de Gemini (múltiples conversaciones):", contenido)
    
    # Limpiar contenido de markdown si existe
    if "```json" in contenido:
        contenido = contenido.split("```json")[1].split("```")[0].strip()
    elif "```" in contenido:
        contenido = contenido.split("```")[1].split("```")[0].strip()
    
    print("Contenido limpio para parsear (múltiples conversaciones):", contenido)

    import json
    try:
        resultado = json.loads(contenido)
        print("JSON parseado exitosamente (múltiples conversaciones):", resultado)
        return resultado
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON de múltiples conversaciones: {e}")
        print(f"Contenido que falló: {contenido}")
        return {
            "prioridad": "media",
            "tono": "amigable", 
            "accion_principal": "Confirmar disponibilidad y fechas específicas",
            "mensaje_sugerido": f"¡Hola! Veo que es tu {len(conversaciones)}ª consulta. Te ayudo inmediatamente con tu reserva.",
            "alerta": f"Cliente recurrente - {len(conversaciones)} conversaciones"
        }
    except Exception as e:
        print(f"Error inesperado en múltiples conversaciones: {e}")
        return {
            "prioridad": "media",
            "tono": "amigable",
            "accion_principal": "Confirmar disponibilidad y fechas específicas", 
            "mensaje_sugerido": f"¡Hola! Veo que es tu {len(conversaciones)}ª consulta. Te ayudo inmediatamente con tu reserva.",
            "alerta": f"Cliente recurrente - {len(conversaciones)} conversaciones"
        }


    def sugerir_acciones_recepcionista(sentimiento, intencion_compra, urgencia, mensajes, id_context=None):
        if not GEMINI_API_KEY:
            raise Exception("GEMINI_API_KEY no está configurada")

        # Unimos los mensajes para dar contexto
        historial = ""
        for i, m in enumerate(mensajes, 1):
            historial += f"Mensaje {i}: {m}\n"

        prompt = f"""
        # Rol
        Eres un experto en atención al cliente hotelero y gestor de experiencias. Tu tarea es proporcionar sugerencias específicas y prácticas para que un recepcionista atienda de manera óptima a este cliente según su perfil emocional y comercial.

        # Análisis del cliente
        - **Sentimiento**: {sentimiento}
        - **Intención de compra**: {intencion_compra}
        - **Urgencia**: {urgencia}
        - **ID del contexto**: {id_context or "No especificado"}

        # Mensajes del cliente:
        {historial}

        # Tu tarea
        Basándote en el análisis, proporciona sugerencias específicas y accionables para el recepcionista, incluyendo el tono a usar, qué ofrecer, cómo manejar la situación y pasos concretos a seguir.

        # Guías específicas:

        ## Por URGENCIA:
        **Alta**: Respuesta inmediata, facilitar proceso, confirmar disponibilidad al instante
        **Media**: Respuesta pronta pero con más detalles, ofrecer opciones
        **Baja**: Respuesta completa con información educativa

        ## Por INTENCIÓN DE COMPRA:
        **Alta**: Enfocar en cerrar venta, minimizar fricción, acelerar proceso de reserva
        **Media**: Nutrir con información valiosa, construir confianza, ofrecer opciones
        **Baja**: Educación sobre valor, crear interés, seguimiento de largo plazo

        ## Por SENTIMIENTO:
        **Contento**: Mantener buena energía, aprovechar momentum positivo
        **Enojado**: Empatía, resolución de problemas, gestos de buena voluntad
        **Neutral**: Crear conexión emocional, destacar beneficios únicos

        # Formato de respuesta
        Responde en formato JSON con esta estructura exacta:
        {{
            "tono_conversacion": "formal/amigable/empático/profesional",
            "prioridad_respuesta": "inmediata/rapida/normal",
            "acciones_inmediatas": ["acción1", "acción2", "acción3"],
            "informacion_a_solicitar": ["dato1", "dato2", "dato3"],
            "scripts_respuesta": {{
                "apertura": "Primer mensaje de respuesta sugerido",
                "seguimiento": "Mensaje de seguimiento si no responde",
                "cierre": "Mensaje para cerrar la conversación"
            }},
        }}
        """

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
        
        print("Respuesta cruda de Gemini (recepcionista):", contenido)
        
        # Limpiar contenido de markdown si existe
        if "```json" in contenido:
            contenido = contenido.split("```json")[1].split("```")[0].strip()
        elif "```" in contenido:
            contenido = contenido.split("```")[1].split("```")[0].strip()
        
        print("Contenido limpio para parsear (recepcionista):", contenido)

        import json
        try:
            resultado = json.loads(contenido)
            print("JSON parseado exitosamente (recepcionista):", resultado)
            return resultado
        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON de recepcionista: {e}")
            print(f"Contenido que falló: {contenido}")
            return {
                "saludo_recomendado": "¡Hola! Gracias por contactarnos, estaré encantado de ayudarte.",
                "tono_conversacion": "amigable",
                "prioridad_respuesta": "normal",
                "acciones_inmediatas": ["Confirmar disponibilidad", "Solicitar fechas específicas", "Ofrecer opciones"],
                "informacion_a_solicitar": ["Fechas de estancia", "Número de huéspedes", "Preferencias especiales"],
                "ofertas_sugeridas": ["Descuento por reserva anticipada", "Upgrade gratuito", "Desayuno incluido"],
                "scripts_respuesta": {
                    "apertura": "¡Hola! Muchas gracias por tu interés en nuestro hotel. ¿En qué fechas estarías interesado en hospedarte?",
                    "seguimiento": "¿Tienes alguna pregunta adicional? Estoy aquí para ayudarte con cualquier información que necesites.",
                    "cierre": "¡Perfecto! He guardado toda tu información. Te enviaré la confirmación por email. ¡Esperamos verte pronto!"
                },
                "alertas_especiales": ["Cliente potencial", "Seguimiento requerido"],
                "tiempo_respuesta_maximo": "4 horas",
                "derivar_a": "ninguno",
                "notas_internas": "Cliente con intención de reserva, mantener seguimiento activo"
            }
        except Exception as e:
            print(f"Error inesperado en recepcionista: {e}")
            return {
                "saludo_recomendado": "¡Hola! Gracias por contactarnos, estaré encantado de ayudarte.",
                "tono_conversacion": "amigable",
                "prioridad_respuesta": "normal",
                "acciones_inmediatas": ["Confirmar disponibilidad", "Solicitar fechas específicas", "Ofrecer opciones"],
                "informacion_a_solicitar": ["Fechas de estancia", "Número de huéspedes", "Preferencias especiales"],
                "ofertas_sugeridas": ["Descuento por reserva anticipada", "Upgrade gratuito", "Desayuno incluido"],
                "scripts_respuesta": {
                    "apertura": "¡Hola! Muchas gracias por tu interés en nuestro hotel. ¿En qué fechas estarías interesado en hospedarte?",
                    "seguimiento": "¿Tienes alguna pregunta adicional? Estoy aquí para ayudarte con cualquier información que necesites.",
                    "cierre": "¡Perfecto! He guardado toda tu información. Te enviaré la confirmación por email. ¡Esperamos verte pronto!"
                },
                "alertas_especiales": ["Cliente potencial", "Seguimiento requerido"],
                "tiempo_respuesta_maximo": "4 horas",
                "derivar_a": "ninguno",
                "notas_internas": "Cliente con intención de reserva, mantener seguimiento activo"
            }