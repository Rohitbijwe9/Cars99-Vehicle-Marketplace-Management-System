from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        
        # Use 'username' as 'email' since Django admin always sends 'username'
        email = username  

        try:
            user = User.objects.get(email=email)  # ✅ Query user by email
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

        return None
