
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.apps import apps

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 1. Obtener el header Authorization
        header = request.headers.get('Authorization')
        if not header:
            return None # No hay token, pasa a la siguiente verificación

        try:
            # El formato debe ser "Bearer <token>"
            token_type, token_str = header.split()
            if token_type != 'Bearer':
                return None
        except ValueError:
            return None

        # 2. Validar el token y decodificar
        try:
            token = AccessToken(token_str)
            user_id = token['user_id'] # Extraemos el ID que guardaremos al loguear
        except Exception as e:
            raise AuthenticationFailed('Token inválido o expirado')

        # 3. Buscar tu usuario personalizado
        Usuario = apps.get_model('usuarios', 'Usuario')
        try:
            usuario = Usuario.objects.get(u_id=user_id)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')

        # 4. Retornar la tupla (usuario, token) para que request.user funcione
        return (usuario, token)
