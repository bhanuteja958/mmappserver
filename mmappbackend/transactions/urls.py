from django.urls import path
from . import views


urlpatterns = [
    path('static_data/', views.TrasactionsStaticData.as_view()),
    path('<str:pk>/', views.Transactions.as_view()),
    path('<int:month>/<int:year>/', views.TransactionList.as_view()),
    path('aggregations/<int:month>/<int:year>/', views.TransactionAggregations.as_view()),
    path('', views.TransactionList.as_view(), {"month":None, "year": None})
]