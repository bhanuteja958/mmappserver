from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount','description','created_date','modified_date','user_id','category','transaction_type', 'payment_mode']
    