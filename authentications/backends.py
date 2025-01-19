from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model



class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        # Try to fetch the user by username
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # Try to fetch the user by email
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
