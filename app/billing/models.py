from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import uuid


class Plan(models.Model):
    PLAN_TYPES = [
        ("basic", "Basic"),
        ("pro", "Pro"),
        ("enterprise", "Enterprise"),
    ]

    BILLING_CYCLES = [
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(
        max_length=20, choices=BILLING_CYCLES, default="monthly"
    )
    features = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    stripe_price_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.price}/{self.billing_cycle}"

    class Meta:
        ordering = ["price"]


class Subscription(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
        ("pending", "Pending"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="subscriptions"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    next_billing_date = models.DateTimeField()
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.next_billing_date:
            if self.plan.billing_cycle == "monthly":
                self.next_billing_date = self.start_date + timedelta(days=30)
            else:
                self.next_billing_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)

    def is_active(self):
        return self.status == "active" and (
            not self.end_date or self.end_date > timezone.now()
        )

    def cancel(self):
        self.status = "cancelled"
        self.end_date = timezone.now()
        self.save()

    class Meta:
        ordering = ["-created_at"]


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("overdue", "Overdue"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices"
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="invoices"
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    paid_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    stripe_invoice_id = models.CharField(max_length=100, blank=True)
    payment_intent_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.user.email} - ${self.amount}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.issue_date + timedelta(days=30)  # 30 days to pay
        if not self.amount:
            self.amount = self.plan.price
        super().save(*args, **kwargs)

    def mark_paid(self):
        self.status = "paid"
        self.paid_date = timezone.now()
        self.save()

    def is_overdue(self):
        return self.status == "pending" and self.due_date < timezone.now()

    class Meta:
        ordering = ["-created_at"]


class PaymentReminder(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="reminders"
    )
    sent_date = models.DateTimeField(default=timezone.now)
    reminder_type = models.CharField(max_length=50, default="payment_due")
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for Invoice {self.invoice.id}"

    class Meta:
        ordering = ["-created_at"]
