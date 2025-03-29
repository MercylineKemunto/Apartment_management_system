from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ApartmentViewSet, UnitViewSet, LeaseViewSet, 
    PaymentViewSet, DebtViewSet, MaintenanceRequestViewSet, 
    ExpenseViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'apartments', ApartmentViewSet)
router.register(r'units', UnitViewSet)
router.register(r'leases', LeaseViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'debts', DebtViewSet)
router.register(r'maintenance-requests', MaintenanceRequestViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('maintenance_requests/', MaintenanceRequestViewSet.as_view({'get': 'list', 'post': 'create'}), name='maintenance_requests_list'),
]