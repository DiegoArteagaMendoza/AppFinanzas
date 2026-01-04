from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.apps import apps

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header:
            return None

        try:
            token_type, token_str = header.split()
            if token_type != 'Bearer':
                return None
        except ValueError:
            return None
        try:
            token = AccessToken(token_str)
            user_id = token['user_id']
        except Exception as e:
            raise AuthenticationFailed('Token inválido o expirado')
        Usuario = apps.get_model('usuarios', 'Usuario')
        try:
            usuario = Usuario.objects.get(u_id=user_id)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')
        return (usuario, token)
