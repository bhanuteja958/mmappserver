from django.urls import path
from . import views


urlpatterns = [
    path('', views.TransactionList.as_view())
]