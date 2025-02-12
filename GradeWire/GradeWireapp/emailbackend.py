from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class emailbackend(ModelBackend):
    def authenticate(self,username=None,password=None,**kwargs):
        UserModel=get_user_model()
        try:
            user=UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_passsword(password):
                return user
            return None 