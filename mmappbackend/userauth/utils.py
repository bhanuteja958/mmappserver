from django.contrib.auth.models import User

def create_new_user(username,email,password):
    user = User.objects.create_user(username,email,password)
    return {
        "email": user.email,
        "user_name": user.username
    }