from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework import status
from rest_framework.views import APIView
from .models import Transaction
from .serializers import TransactionSerializer
from global_utils import getAPIResponse


class TransactionList(APIView):
    authentication_classes=[ authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, month, year):
        transactions = Transaction.objects.filter(user=request.user, created_date__year = year, created_date__month = month)
        serializer = TransactionSerializer(transactions, many=True)
        transactions_by_date = {}
        for transaction in serializer.data:
            transactionDate = transaction["created_date"].split('T')[0]
            if transactionDate not in transactions_by_date:
                transactions_by_date[transactionDate] = []
            transactions_by_date[transactionDate].append(transaction)
        return Response(
            getAPIResponse(False, 'successfully fetched data', data=transactions_by_date),
            status=status.HTTP_200_OK
        )
    
    def post(self,request, month, year):
        serializer = TransactionSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                getAPIResponse(False, 'Successfully created transaction'),
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                getAPIResponse(True, 'Error while creating transaction',errors=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )
  
class Transactions(APIView):
    authentication_classes=[ authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk)
            serializer = TransactionSerializer(transaction)
            return Response(
                getAPIResponse(False, "Successfully fetched transaction",data=serializer.data), 
                status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response(getAPIResponse(True, 'No transactions with the given id exists'), status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk)
            if(transaction.user != request.user):
                return Response(
                    getAPIResponse(True, "You don't have permission to edit this transaction"),
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = TransactionSerializer(transaction, data=request.POST, partial=True)
            if serializer.is_valid():
                
                serializer.save()
                return Response(
                    getAPIResponse(False, 'Transaction successfully updated'),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                     getAPIResponse(False, 'Error while updating transaction', errors=serializer.errors),
                     status=status.HTTP_400_BAD_REQUEST
                )
        except Transaction.DoesNotExist:
            return Response(
                getAPIResponse(True, 'No transactions with the given id exists'),
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk)
            if(transaction.user != request.user):
                return Response(
                    getAPIResponse(True, "You don't have permission to delete this transaction"),
                    status=status.HTTP_403_FORBIDDEN
                )
            transaction.delete()
            return Response(
                getAPIResponse(False, 'Successfully deleted transaction'),
                status=status.HTTP_200_OK
            )
        except Transaction.DoesNotExist:
            return Response(
                getAPIResponse(True, 'No transactions with the given id exists'),
                status=status.HTTP_200_OK
            ) 
        