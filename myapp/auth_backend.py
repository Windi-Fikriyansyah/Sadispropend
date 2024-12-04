# myapp/auth_backend.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from myapp.models import TblUser

class TblUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = TblUser.objects.get(username=username)
            if user.password == password:  # In real applications, hash and compare passwords
                return user
        except TblUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return TblUser.objects.get(pk=user_id)
        except TblUser.DoesNotExist:
            return None
