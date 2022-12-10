from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Transaction, Category, PaymentMode, TransactionType

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = ['id', 'mode_name']

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['id', 'type_name']

class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    transaction_type = serializers.CharField(source='transaction_type.type_name', read_only=True)
    payment_mode = serializers.CharField(source='payment_mode.mode_name', read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    transaction_type_id = serializers.IntegerField(write_only=True)
    payment_mode_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Transaction
        fields = ['id', 'amount','description','created_date','modified_date','category','transaction_type', 'payment_mode', 'category_id','transaction_type_id','payment_mode_id']
    
    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.description = validated_data.get('description', instance.description)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.transaction_type_id = validated_data.get('transaction_type_id',instance.transaction_type_id)
        instance.payment_mode_id = validated_data.get('payment_mode_id',instance.payment_mode_id)
        instance.save()
        return instance


    