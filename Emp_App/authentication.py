from rest_framework.authentication import BaseAuthentication
from Emp_App.models import BlackListedToken
from rest_framework import exceptions

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            jwt_token = request.headers["Authorization"].split()[1]   
            user_session = BlackListedToken.objects.filter(token = jwt_token)
            if not user_session.exists():
                raise exceptions.AuthenticationFailed("JWT Authentication Failed")
            user_obj = user_session.first().user
            return (user_obj, jwt_token)
        except:
            raise exceptions.AuthenticationFailed("JWT Authentication Failed")
