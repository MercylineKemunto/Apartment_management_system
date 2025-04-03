from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Apartment, Unit, Lease, Payment, 
    Debt, MaintenanceRequest, Expense, Notification
)

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'manager', 'created_at']
    search_fields = ['name', 'address']

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'apartment', 'size', 'rent_amount', 'is_occupied')
    list_filter = ('apartment', 'is_occupied')
    search_fields = ('unit_number', 'apartment__name')
    list_editable = ('is_occupied',)
    ordering = ('apartment', 'unit_number')

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'unit', 'start_date', 'end_date', 'rent_due_date']
    list_filter = ['start_date', 'end_date']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['lease', 'amount', 'payment_date', 'payment_method']
    list_filter = ['payment_method']

@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ['lease', 'amount', 'due_date', 'is_paid']
    list_filter = ['is_paid']

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['unit', 'description', 'request_date', 'status']
    list_filter = ['status']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['apartment', 'description', 'amount', 'date_incurred']
    list_filter = ['apartment']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at', 'is_read']
    list_filter = ['is_read']

# Register other models if not already registered
admin.site.register(Apartment)
admin.site.register(Lease)
admin.site.register(Payment)
admin.site.register(Debt)
admin.site.register(MaintenanceRequest)
admin.site.register(Expense)
admin.site.register(Notification)
