import os
from functools import wraps
from django.http import JsonResponse

def require_api_key(view_func):
    """
    Decorador que requiere una API Key válida en el header 'X-API-Key'
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Obtener la API Key del header
        api_key = request.headers.get('X-API-Key')
        
        # Obtener la API Key válida del entorno
        valid_api_key = os.getenv('API_KEY')
        
        # Verificar si la API Key es válida
        if not api_key:
            return JsonResponse(
                {"error": "API Key requerida. Incluye el header 'X-API-Key'."}, 
                status=401
            )
        
        if api_key != valid_api_key:
            return JsonResponse(
                {"error": "API Key inválida."}, 
                status=403
            )
        
        # Si la API Key es válida, ejecutar la vista
        return view_func(request, *args, **kwargs)
    
    return wrapper
