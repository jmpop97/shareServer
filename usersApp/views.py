from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from usersApp.serializers import CustomTokenObtainPairSerializer
import os
from django.http import JsonResponse
front_url= os.environ.get("URL_FRONTEND")
class UserView(APIView):
    def get(self, request, format=None):
        print(request.user)
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
class UserLogout(APIView):
    def post(self,request,format=None):
        print("UserLogout work")
        response = JsonResponse({'message': 'Logged out'})
        response.delete_cookie('jwt_access')  # 삭제해야 하는 쿠키 이름
        return response
class CustomTokenObtainPairView(TokenObtainPairView):
    renderer_classes = [JSONRenderer]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            print("Response data:", response.data)
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            if access_token and refresh_token:
                response.set_cookie(
                    key='jwt_access',
                    value=access_token,
                    secure=True,
                    samesite='Lax'
                )
                response.set_cookie(
                    key='jwt_refresh',
                    value=refresh_token,
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
