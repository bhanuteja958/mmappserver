from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework import status
from rest_framework.views import APIView
from .models import Transaction, Category, PaymentMode, TransactionType
from .serializers import TransactionSerializer, CategorySerializer, PaymentModeSerializer, TransactionTypeSerializer
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
        print(request.data)
        serializer = TransactionSerializer(data=request.data)
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

class TransactionAggregations(APIView):
    authentication_classes=[ authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, month, year):
        transactionAggregations = dict()
        transactionAggregations['income'] = 0
        transactionAggregations['expenses'] = 0
        transactionSerializer = Transaction.objects.filter(user = request.user, created_date__year = year, created_date__month = month)
        transactions = TransactionSerializer(transactionSerializer, many=True)

        if len(transactions.data) == 0:
            return Response(
                getAPIResponse(
                    False, 'No Transactions added for the given month', data={}
                ),
                status=status.HTTP_200_OK
            )
        
        for transaction in transactions.data:
            if transaction['transaction_type'] == 'expense':
                transactionAggregations['expenses'] += transaction['amount']
            else:
                transactionAggregations['income'] += transaction['amount']
            paymentMode = transaction['payment_mode']
            if  paymentMode  not in transactionAggregations.keys():
                transactionAggregations[paymentMode] = 0
            transactionAggregations[paymentMode] += transaction['amount']
        
        transactionAggregations['balance'] = transactionAggregations['income'] - transactionAggregations['expenses']

        return Response(
            getAPIResponse(
                False, 'successfully fetched transactions', data=transactionAggregations
            ),
            status = status.HTTP_200_OK
        )
class TrasactionsStaticData(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request):
        
        categorySerializer = CategorySerializer(Category.objects.all(),many=True)
        paymentModeSerializer = PaymentModeSerializer(PaymentMode.objects.all(), many=True)
        transactionTypeSerializer = TransactionTypeSerializer(TransactionType.objects.all(), many=True)
        return Response(    
            getAPIResponse(False, 'Successfully fetched static data', data={
                "categories": categorySerializer.data,
                "paymentModes": paymentModeSerializer.data,
                "transactionTypes":transactionTypeSerializer.data
            })
        )

