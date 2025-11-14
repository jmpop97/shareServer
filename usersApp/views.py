from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from usersApp.serializers import CustomTokenObtainPairSerializer
front_url="http://127.0.0.1:5500/html"
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
        try:
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
            response['Location'] = front_url+'/main.html'  # Redirect to /main.html
            response.status_code = 302  # HTTP status for redirection
            return response
        except AuthenticationFailed:
            response= Response(
                {'success': False, 'detail': 'Invalid credentials'},
                status=401
            )
            response['Location'] = front_url+"/login.html"
            response.status_code = 302
            return response
