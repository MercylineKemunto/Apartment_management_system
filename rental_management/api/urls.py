from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.routers import DefaultRouter
from .views import (
    ApartmentViewSet, UnitViewSet, LeaseViewSet, 
    PaymentViewSet, DebtViewSet, MaintenanceRequestViewSet, 
    ExpenseViewSet, NotificationViewSet, UserViewSet
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
    path('maintenance_requests/', MaintenanceRequestViewSet.as_view({'get': 'list', 'post': 'create'}), name='maintenance_requests_list'),
    path('user/update/', UserViewSet.as_view({'put': 'update'}), name='user-update'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]