from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class NormalUserBackend(ModelBackend):
    """Authentication backend for normal users only (excluding superusers)."""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password) and not user.is_superuser:
                return user
        except User.DoesNotExist:
            return None
        return None

class SuperUserBackend(ModelBackend):
    """Authentication backend for superusers only."""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_superuser:
                return user
        except User.DoesNotExist:
            return None
        return None
