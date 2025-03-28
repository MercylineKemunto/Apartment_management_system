from rest_framework import serializers
from .models import (
    Apartment, Unit, Lease, Payment, 
    Debt, MaintenanceRequest, Expense, Notification
)
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ApartmentSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)
    units_count = serializers.SerializerMethodField()

    class Meta:
        model = Apartment
        fields = ['id', 'name', 'address', 'manager', 'created_at', 'units_count']

    def get_units_count(self, obj):
        return obj.units.count()

class UnitSerializer(serializers.ModelSerializer):
    apartment = ApartmentSerializer(read_only=True)

    class Meta:
        model = Unit
        fields = ['id', 'apartment', 'unit_number', 'size', 'rent_amount', 'is_occupied']

class LeaseSerializer(serializers.ModelSerializer):
    tenant = UserSerializer(read_only=True)
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Lease
        fields = ['id', 'tenant', 'unit', 'start_date', 'end_date', 'rent_due_date']

class PaymentSerializer(serializers.ModelSerializer):
    lease = LeaseSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'lease', 'amount', 'payment_date', 'payment_method']

class DebtSerializer(serializers.ModelSerializer):
    lease = LeaseSerializer(read_only=True)

    class Meta:
        model = Debt
        fields = ['id', 'lease', 'amount', 'due_date', 'is_paid']

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'unit', 'description', 'request_date', 'status']

class ExpenseSerializer(serializers.ModelSerializer):
    apartment = ApartmentSerializer(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'apartment', 'description', 'amount', 'date_incurred']

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'is_read']