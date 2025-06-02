import stripe
from django.conf import settings
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from app.billing.models import Plan, Subscription, Invoice
from app.billing.serializers import (
    PlanSerializer,
    SubscriptionSerializer,
    SubscriptionCreateSerializer,
    InvoiceSerializer,
)


# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class PlanListView(generics.ListAPIView):
    """
    List all available plans
    """

    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer
    permission_classes = []


class SubscriptionListView(generics.ListAPIView):
    """
    List user's subscriptions
    """

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user).select_related(
            "plan"
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def subscribe_to_plan(request):
    """
    Subscribe user to a plan
    """
    serializer = SubscriptionCreateSerializer(data=request.data)
    if serializer.is_valid():
        plan = serializer.validated_data["plan"]

        existing_subscription = Subscription.objects.filter(
            user=request.user, status="active"
        ).first()

        if existing_subscription:
            return Response(
                {"error": "You already have an active subscription"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription = Subscription.objects.create(
            user=request.user, plan=plan, status="active", start_date=timezone.now()
        )

        first_invoice = Invoice.objects.create(
            user=request.user,
            subscription=subscription,
            plan=plan,
            amount=plan.price,
            issue_date=timezone.now(),
        )

        return Response(
            {
                "message": "Successfully subscribed to plan",
                "subscription": SubscriptionSerializer(subscription).data,
                "invoice": InvoiceSerializer(first_invoice).data,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unsubscribe(request, subscription_id):
    """
    Cancel user's subscription
    """
    subscription = get_object_or_404(
        Subscription, id=subscription_id, user=request.user
    )

    if subscription.status != "active":
        return Response(
            {"error": "Subscription is not active"}, status=status.HTTP_400_BAD_REQUEST
        )

    subscription.cancel()

    return Response(
        {
            "message": "Subscription cancelled successfully",
            "subscription": SubscriptionSerializer(subscription).data,
        },
        status=status.HTTP_200_OK,
    )


class InvoiceListView(generics.ListAPIView):
    """
    List user's invoices
    """

    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user).select_related(
            "plan", "subscription"
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def invoice_detail(request, invoice_id):
    """
    Get invoice details
    """
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    serializer = InvoiceSerializer(invoice)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def pay_invoice(request, invoice_id):
    """
    Pay an invoice (mock implementation)
    """
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)

    if invoice.status != "pending" and invoice.status != "overdue":
        return Response(
            {"error": "Invoice cannot be paid"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        invoice.mark_paid()

        return Response(
            {
                "message": "Payment processed successfully",
                "invoice": InvoiceSerializer(invoice).data,
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {"error": f"Payment processing failed: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_stripe_payment_intent(request, invoice_id):
    """
    Create Stripe payment intent for invoice
    """
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)

    if invoice.status not in ["pending", "overdue"]:
        return Response(
            {"error": "Invoice cannot be paid"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        if not request.user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=request.user.email,
                name=request.user.username,
            )
            request.user.stripe_customer_id = customer.id
            request.user.save()

        intent = stripe.PaymentIntent.create(
            amount=int(invoice.amount * 100),
            currency="usd",
            customer=request.user.stripe_customer_id,
            metadata={
                "invoice_id": str(invoice.id),
                "user_id": str(request.user.id),
            },
        )

        invoice.payment_intent_id = intent.id
        invoice.save()

        return Response(
            {"client_secret": intent.client_secret, "payment_intent_id": intent.id},
            status=status.HTTP_200_OK,
        )

    except stripe.error.StripeError as e:
        return Response(
            {"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def billing_dashboard(request):
    """
    Get user's billing dashboard data
    """
    user = request.user

    active_subscription = (
        Subscription.objects.filter(user=user, status="active")
        .select_related("plan")
        .first()
    )

    recent_invoices = (
        Invoice.objects.filter(user=user)
        .select_related("plan")
        .order_by("-created_at")[:5]
    )

    pending_invoices = Invoice.objects.filter(
        user=user, status__in=["pending", "overdue"]
    ).select_related("plan")

    total_owed = sum(invoice.amount for invoice in pending_invoices)

    return Response(
        {
            "active_subscription": (
                SubscriptionSerializer(active_subscription).data
                if active_subscription
                else None
            ),
            "recent_invoices": InvoiceSerializer(recent_invoices, many=True).data,
            "pending_invoices": InvoiceSerializer(pending_invoices, many=True).data,
            "total_owed": total_owed,
            "next_billing_date": (
                active_subscription.next_billing_date if active_subscription else None
            ),
        }
    )
