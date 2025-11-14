import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()

class CookieJWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('jwt_access')
        print("work")
        if not token:
            return

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user = User.objects.get(id=payload['user_id'])
            print(request.user)
        except:
            pass