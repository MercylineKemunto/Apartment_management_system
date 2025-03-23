from django.db import models
from django.contrib.auth.models import User

class Apartment(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_apartments')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Unit(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=10)
    size = models.DecimalField(max_digits=5, decimal_places=2)  # Size in square meters
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.unit_number} - {self.apartment.name}"


class Lease(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leases')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='leases')
    start_date = models.DateField()
    end_date = models.DateField()
    rent_due_date = models.DateField()

    def __str__(self):
        return f"Lease for {self.tenant.username} in {self.unit.unit_number}"


class Payment(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)  

    def __str__(self):
        return f"Payment of {self.amount} for {self.lease}"


class Debt(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='debts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Debt of {self.amount} for {self.lease}"


class MaintenanceRequest(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='maintenance_requests')
    description = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Open') 

    def __str__(self):
        return f"Maintenance request for {self.unit.unit_number}"


class Expense(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_incurred = models.DateField()

    def __str__(self):
        return f"Expense: {self.description} for {self.apartment.name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}..."
