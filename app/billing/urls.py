from django.urls import path
from app.billing import views

urlpatterns = [
    path("plans/", views.PlanListView.as_view(), name="plan-list"),
    path(
        "subscriptions/", views.SubscriptionListView.as_view(), name="subscription-list"
    ),
    path("subscribe/", views.subscribe_to_plan, name="subscribe"),
    path(
        "subscriptions/<uuid:subscription_id>/cancel/",
        views.unsubscribe,
        name="unsubscribe",
    ),
    path("invoices/", views.InvoiceListView.as_view(), name="invoice-list"),
    path("invoices/<uuid:invoice_id>/", views.invoice_detail, name="invoice-detail"),
    path("invoices/<uuid:invoice_id>/pay/", views.pay_invoice, name="pay-invoice"),
    path(
        "invoices/<uuid:invoice_id>/stripe-payment/",
        views.create_stripe_payment_intent,
        name="stripe-payment",
    ),
    path("dashboard/", views.billing_dashboard, name="billing-dashboard"),
]
