from django.urls import path
from . import views


urlpatterns = [
    path('<int:month>/<int:year>/', views.TransactionList.as_view()),
    path('<str:pk>/', views.Transactions.as_view()),
    path('', views.TransactionList.as_view(), {"month":None, "year": None})
]