from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "category"

class PaymentMode(models.Model):
    mode_name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payment_mode"

class TransactionType(models.Model):
    type_name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction_type'

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.CASCADE)

    class Meta:
        db_table = 'transactions'



