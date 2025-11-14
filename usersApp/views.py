from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from usersApp.serializers import CustomTokenObtainPairSerializer
class UserView(APIView):
    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')
        if access_token and refresh_token:
            response.set_cookie(
                key='jwt_access',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            response.set_cookie(
                key='jwt_refresh',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='Lax'
            )
        response.data = {'success': True}
        return response
class AuthView(APIView):
    def post(self,request):
        data = request.data
        username = data.get('id')
        password = data.get('pwd')

        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid credentials')

        response = Response({
            'message': 'Login successful',
            # "value":token.key
            })
        response.set_cookie(key='jwt', value="jwt", httponly=True)
        return response