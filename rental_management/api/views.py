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
from django.utils import timezone
from rest_framework.response import Response
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

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
    template_name = 'units/list.html'

    def get_template_names(self):
        if self.action == 'list':
            return ['units/list.html']
        elif self.action == 'create':
            return ['units/create.html']
        elif self.action == 'update':
            return ['units/edit.html']
        elif self.action == 'destroy':
            return ['units/delete.html']
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apartments'] = Apartment.objects.all()
        return context

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
    template_name = 'payments/list.html'

    def get_template_names(self):
        if self.action == 'list':
            return ['payments/list.html']
        elif self.action == 'create':
            return ['payments/create.html']
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leases'] = Lease.objects.all()
        return context

    def create(self, request, *args, **kwargs):
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = request.data
        else:
            data = request.POST

        lease_id = data.get('lease')
        amount = data.get('amount')
        payment_method = data.get('payment_method')

        if not lease_id or not amount or not payment_method:
            return Response(
                {'error': 'lease, amount, and payment_method are required'},
                status=400
            )

        try:
            lease = Lease.objects.get(id=lease_id)
            payment = Payment.objects.create(
                lease=lease,
                amount=amount,
                payment_method=payment_method
            )
            
            if request.content_type == 'application/json':
                return Response(PaymentSerializer(payment).data, status=201)
            else:
                return redirect('payment-list')
                
        except Lease.DoesNotExist:
            return Response({'error': 'Lease not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

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
   

def is_tenant(user):
    return user.groups.filter(name='Tenant').exists()

@login_required
def tenant_dashboard(request):
    if not is_tenant(request.user):
        return redirect('dashboard')
    
    current_lease = Lease.objects.filter(tenant=request.user, end_date__gte=timezone.now().date()).first()
    maintenance_requests = MaintenanceRequest.objects.filter(unit__leases__tenant=request.user).order_by('-request_date')[:5]
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Calculate total outstanding amount
    total_outstanding = 0
    next_payment_due = None
    if current_lease:
        total_outstanding = Debt.objects.filter(
            lease=current_lease,
            is_paid=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        next_payment = Debt.objects.filter(
            lease=current_lease,
            is_paid=False
        ).order_by('due_date').first()
        if next_payment:
            next_payment_due = next_payment.due_date
    
    context = {
        'current_lease': current_lease,
        'maintenance_requests': maintenance_requests,
        'notifications': notifications,
        'total_outstanding': total_outstanding,
        'next_payment_due': next_payment_due,
    }
    return render(request, 'tenants/dashboard.html', context)

@login_required
def tenant_payments(request):
    if not is_tenant(request.user):
        return redirect('dashboard')
    
    current_lease = Lease.objects.filter(tenant=request.user, end_date__gte=timezone.now().date()).first()
    if not current_lease:
        return redirect('tenant_dashboard')
    
    payments = Payment.objects.filter(lease=current_lease).order_by('-payment_date')
    debts = Debt.objects.filter(lease=current_lease).order_by('-due_date')
    
    context = {
        'payments': payments,
        'debts': debts,
        'current_lease': current_lease,
    }
    return render(request, 'tenants/payments.html', context)

@login_required
def make_payment(request):
    if not is_tenant(request.user):
        return redirect('dashboard')
    
    current_lease = Lease.objects.filter(tenant=request.user, end_date__gte=timezone.now().date()).first()
    if not current_lease:
        return redirect('tenant_dashboard')
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        
        if amount and payment_method:
            Payment.objects.create(
                lease=current_lease,
                amount=amount,
                payment_method=payment_method
            )
            return redirect('tenant_payments')
    
    context = {
        'current_lease': current_lease,
        'payment_methods': ['Credit Card', 'Bank Transfer', 'Cash'],
    }
    return render(request, 'tenants/make_payment.html', context)

@login_required
def create_maintenance_request(request):
    if request.method == 'POST':
        unit_id = request.POST.get('unit')
        description = request.POST.get('description')
        status = request.POST.get('status', 'Open')
        
        if not unit_id:
            return render(request, 'maintenance_requests/create.html', {
                'units': Unit.objects.all(),
                'error': 'Please select a unit'
            })
            
        unit = get_object_or_404(Unit, id=unit_id)
        MaintenanceRequest.objects.create(
            unit=unit,
            description=description,
            status=status
        )
        return redirect('maintenance_requests_list')
        
    return render(request, 'maintenance_requests/create.html', {
        'units': Unit.objects.all()
    })

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
    units = Unit.objects.all()
    context = {
        'title': 'Units List',
        'units': units
    }
    return render(request, 'units/list.html', context)

def leases_list(request):
    leases = Lease.objects.all()
    context = {
        'title': 'Leases List',
        'leases': leases
    }
    return render(request, 'leases/list.html', context)

@login_required
def create_unit(request):
    if request.method == 'POST':
        # Handle unit creation
        pass
    apartments = Apartment.objects.all()
    return render(request, 'units/create.html', {'apartments': apartments})

@login_required
def edit_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        # Handle unit update
        pass
    apartments = Apartment.objects.all()
    return render(request, 'units/edit.html', {
        'unit': unit,
        'apartments': apartments
    })

@login_required
def delete_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        unit.delete()
        return redirect('units_list')
    return render(request, 'units/delete.html', {'unit': unit})

@login_required
def maintenance_requests_list(request):
    requests = MaintenanceRequest.objects.all().order_by('-request_date')
    return render(request, 'maintenance_requests/list.html', {'requests': requests})

@login_required
def create_lease(request):
    if request.method == 'POST':
        tenant = get_object_or_404(User, id=request.POST['tenant'])
        unit = get_object_or_404(Unit, id=request.POST['unit'])
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        rent_due_date = request.POST['rent_due_date']
        
        lease = Lease.objects.create(
            tenant=tenant,
            unit=unit,
            start_date=start_date,
            end_date=end_date,
            rent_due_date=rent_due_date
        )
        unit.is_occupied = True
        unit.save()
        return redirect('leases_list')
        
    units = Unit.objects.filter(is_occupied=False)
    tenants = User.objects.filter(groups__name='Tenant')
    return render(request, 'leases/create.html', {
        'units': units,
        'tenants': tenants
    })

@login_required
def edit_lease(request, pk):
    lease = get_object_or_404(Lease, pk=pk)
    if request.method == 'POST':
        tenant = get_object_or_404(User, id=request.POST['tenant'])
        unit = get_object_or_404(Unit, id=request.POST['unit'])
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        rent_due_date = request.POST['rent_due_date']
        
        # If unit is changing, update the old unit's occupied status
        if lease.unit != unit:
            lease.unit.is_occupied = False
            lease.unit.save()
            unit.is_occupied = True
            unit.save()
        
        lease.tenant = tenant
        lease.unit = unit
        lease.start_date = start_date
        lease.end_date = end_date
        lease.rent_due_date = rent_due_date
        lease.save()
        return redirect('leases_list')
        
    units = Unit.objects.all()
    tenants = User.objects.filter(groups__name='Tenant')
    return render(request, 'leases/edit.html', {
        'lease': lease,
        'units': units,
        'tenants': tenants
    })

@login_required
def delete_lease(request, pk):
    lease = get_object_or_404(Lease, pk=pk)
    if request.method == 'POST':
        # Update unit's occupied status before deleting
        lease.unit.is_occupied = False
        lease.unit.save()
        lease.delete()
        return redirect('leases_list')
    return render(request, 'leases/delete.html', {'lease': lease})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/')
    
    def post(self, request):
        logout(request)
        return redirect('/')