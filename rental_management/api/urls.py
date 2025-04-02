from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    ApartmentViewSet, UnitViewSet, LeaseViewSet, 
    PaymentViewSet, DebtViewSet, MaintenanceRequestViewSet, 
    ExpenseViewSet, NotificationViewSet, UserViewSet, LogoutView
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
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apartments/', views.apartments_list, name='apartments_list'),
    path('apartments/<int:pk>/', views.apartment_detail, name='apartment_detail'),
    path('apartments/create/', views.create_apartment, name='create_apartment'),
    path('apartments/<int:pk>/edit/', views.edit_apartment, name='edit_apartment'),
    path('units/', views.units_list, name='units_list'),
    path('units/create/', views.create_unit, name='unit-create'),
    path('units/<int:pk>/edit/', views.edit_unit, name='unit-update'),
    path('units/<int:pk>/delete/', views.delete_unit, name='unit-delete'),
    path('leases/', views.leases_list, name='leases_list'),
    path('leases/create/', views.create_lease, name='create_lease'),
    path('leases/<int:pk>/edit/', views.edit_lease, name='edit_lease'),
    path('leases/<int:pk>/delete/', views.delete_lease, name='delete_lease'),
    path('maintenance-requests/', views.maintenance_requests_list, name='maintenance_requests_list'),
    path('tenants/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('tenants/payments/', views.tenant_payments, name='tenant_payments'),
    path('tenants/payments/make/', views.make_payment, name='make_payment'),
    path('tenants/maintenance/create/', views.create_maintenance_request, name='create_maintenance_request'),
    path('logout/', LogoutView.as_view(), name='logout'),
]