from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Apartment, Unit, Lease, Payment, 
    Debt, MaintenanceRequest, Expense, Notification,
)
from .serializers import (
    ApartmentSerializer, UnitSerializer, LeaseSerializer, 
    PaymentSerializer, DebtSerializer, MaintenanceRequestSerializer, 
    ExpenseSerializer, NotificationSerializer, UserSerializer,
)
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'manager']
    search_fields = ['name', 'address']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['apartment', 'is_occupied']
    search_fields = ['unit_number']

class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tenant', 'unit', 'start_date', 'end_date']
    ordering_fields = ['start_date', 'end_date']

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['lease', 'payment_method']
    ordering_fields = ['payment_date']

class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['lease', 'is_paid']
    ordering_fields = ['due_date']

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['unit', 'status']
    search_fields = ['description']
    template_name = 'maintenance_requests_list.html'  

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['apartment']
    ordering_fields = ['date_incurred']

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'is_read']
    ordering_fields = ['created_at']

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user']
   




@login_required
def dashboard(request):
    total_apartments = Apartment.objects.count()
    total_units = Unit.objects.count()
    occupied_units = Unit.objects.filter(is_occupied=True).count()
    vacant_units = total_units - occupied_units

    
    total_monthly_revenue = Unit.objects.aggregate(total_rent=Sum('rent_amount'))['total_rent'] or 0
    total_outstanding_debts = Debt.objects.filter(is_paid=False).aggregate(total=Sum('amount'))['total'] or 0

    
    open_maintenance_requests = MaintenanceRequest.objects.filter(status='Open').count()
    recent_maintenance_requests = MaintenanceRequest.objects.filter(status='Open')[:5]

   
    recent_leases = Lease.objects.order_by('-start_date')[:5]

    
    upcoming_payments = Debt.objects.filter(is_paid=False).order_by('due_date')[:5]

    context = {
        'total_apartments': total_apartments,
        'occupied_units': occupied_units,
        'vacant_units': vacant_units,
        'total_monthly_revenue': total_monthly_revenue,
        'total_outstanding_debts': total_outstanding_debts,
        'open_maintenance_requests': open_maintenance_requests,
        'recent_maintenance_requests': recent_maintenance_requests,
        'recent_leases': recent_leases,
        'upcoming_payments': upcoming_payments,
    }
    return render(request, 'dashboard.html', context)

@login_required
def apartments_list(request):
    apartments = Apartment.objects.all()
    return render(request, 'apartments/list.html', {'apartments': apartments})

@login_required
def apartment_detail(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    units = apartment.units.all()
    return render(request, 'apartments/detail.html', {
        'apartment': apartment,
        'units': units
    })

@login_required
def create_apartment(request):
    if request.method == 'POST':
       
        pass
    return render(request, 'apartments/create.html')

@login_required
def edit_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.method == 'POST':
        
        pass
    return render(request, 'apartments/edit.html', {'apartment': apartment})
def units_list(request):
   
    context = {
        'title': 'Units List'
    }
    return render(request, 'units_list.html', context)

def leases_list(request):
    
    context = {
        'title': 'Leases List'
    }
    return render(request, 'leases_list.html', context)