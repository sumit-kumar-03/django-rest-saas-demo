from django.contrib import admin
from app.billing.models import Plan, Subscription, Invoice, PaymentReminder


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "plan_type",
        "price",
        "billing_cycle",
        "is_active",
    )
    list_filter = (
        "plan_type",
        "billing_cycle",
        "is_active",
    )
    search_fields = (
        "name",
        "plan_type",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
        "status",
        "start_date",
        "next_billing_date",
    )
    list_filter = ("status", "plan__plan_type")
    search_fields = ("user__email", "user__username")
    readonly_fields = ("id", "created_at", "updated_at")
    date_hierarchy = "start_date"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "amount", "status", "issue_date", "due_date")
    list_filter = ("status", "plan__plan_type")
    search_fields = ("user__email", "user__username")
    readonly_fields = ("id", "created_at", "updated_at")
    date_hierarchy = "issue_date"


@admin.register(PaymentReminder)
class PaymentReminderAdmin(admin.ModelAdmin):
    list_display = ("invoice", "reminder_type", "sent_date", "email_sent")
    list_filter = ("reminder_type", "email_sent")
    readonly_fields = ("id", "created_at")
    date_hierarchy = "sent_date"
