from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)