from django.urls import path
from . import views

urlpatterns = [
    path('register_user/',views.RegisterUser.as_view()),
    path('signin/',views.SignInUser.as_view()),
    path('signout/',views.SignOutUser.as_view())
]