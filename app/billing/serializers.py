from rest_framework import serializers
from app.billing.models import Plan, Subscription, Invoice, PaymentReminder


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_details = PlanSerializer(source="plan", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at", "updated_at")


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("plan",)


class InvoiceSerializer(serializers.ModelSerializer):
    plan_details = PlanSerializer(source="plan", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    subscription_id = serializers.CharField(source="subscription.id", read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "subscription",
            "plan",
            "amount",
            "created_at",
            "updated_at",
        )


class PaymentReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReminder
        fields = "__all__"
        read_only_fields = ("id", "created_at")
