from datetime import timedelta
from django.utils import timezone
from app.logger import logger
from app.celery.celery import saas_project_celery_app
from app.billing.models import Subscription, Invoice, PaymentReminder


@saas_project_celery_app.task(
    acks_late=True,
    autoretry_on=Exception,
    max_retries=3,
    bind=True,
    queue="sheduled_tasks",
)
def generate_invoices_for_active_subscriptions():
    """
    Generate invoices for subscriptions that are due for billing today
    """
    today = timezone.now().date()
    subscriptions = Subscription.objects.filter(
        status="active",
        next_billing_date__date=today,
    )

    invoices_created = 0

    for subscription in subscriptions:
        existing_invoice = Invoice.objects.filter(
            subscription=subscription,
            issue_date__date=today,
        ).first()

        if not existing_invoice:
            invoice = Invoice.objects.create(
                user=subscription.user,
                subscription=subscription,
                plan=subscription.plan,
                amount=subscription.plan.price,
                issue_date=timezone.now(),
                due_date=timezone.now() + timedelta(days=30),
            )

            if subscription.plan.billing_cycle == "monthly":
                subscription.next_billing_date += timedelta(days=30)
            else:
                subscription.next_billing_date += timedelta(days=365)
            subscription.save()

            invoices_created += 1
            logger.info(
                f"Created invoice {invoice.id} for subscription {subscription.id}"
            )

    logger.info(f"Generated {invoices_created} invoices for active subscriptions")
    return f"Generated {invoices_created} invoices"


@saas_project_celery_app.task(
    acks_late=True,
    autoretry_on=Exception,
    max_retries=3,
    bind=True,
    queue="sheduled_tasks",
)
def mark_overdue_invoices():
    """
    Mark invoices as overdue if they are past their due date
    """
    now = timezone.now()
    overdue_invoices = Invoice.objects.filter(status="pending", due_date__lt=now)

    updated_count = overdue_invoices.update(status="overdue")
    logger.info(f"Marked {updated_count} invoices as overdue")
    return f"Marked {updated_count} invoices as overdue"


@saas_project_celery_app.task(
    acks_late=True,
    autoretry_on=Exception,
    max_retries=3,
    bind=True,
    queue="sheduled_tasks",
)
def send_payment_reminders():
    """
    Send payment reminders for overdue invoices
    """
    overdue_invoices = Invoice.objects.filter(status="overdue").select_related(
        "user", "plan"
    )

    reminders_sent = 0

    for invoice in overdue_invoices:
        today = timezone.now().date()
        reminder_exists = PaymentReminder.objects.filter(
            invoice=invoice, sent_date__date=today
        ).exists()

        if not reminder_exists:
            reminder = PaymentReminder.objects.create(
                invoice=invoice, reminder_type="payment_overdue"
            )

            try:
                send_payment_reminder_email(invoice)
                reminder.email_sent = True
                reminder.save()
                reminders_sent += 1
                logger.info(f"Sent payment reminder for invoice {invoice.id}")
            except Exception as e:
                logger.error(
                    f"Failed to send reminder for invoice {invoice.id}: {str(e)}"
                )

    logger.info(f"Sent {reminders_sent} payment reminders")
    return f"Sent {reminders_sent} payment reminders"


def send_payment_reminder_email(invoice):
    """
    Send payment reminder email (mock implementation)
    """
    subject = f"Payment Reminder - Invoice {invoice.id}"
    message = f"""
    Dear {invoice.user.email},
    
    This is a reminder that your payment for {invoice.plan.name} plan is overdue.
    
    Invoice Details:
    - Amount: ${invoice.amount}
    - Due Date: {invoice.due_date.strftime('%Y-%m-%d')}
    - Plan: {invoice.plan.name}
    
    Please make your payment as soon as possible to avoid service interruption.
    
    Thank you,
    Billing Team
    """

    # Mock email sending (print to console in development)
    print(f"SENDING EMAIL TO: {invoice.user.email}")
    print(f"SUBJECT: {subject}")
    print(f"MESSAGE: {message}")
    print("-" * 50)


@saas_project_celery_app.task
def process_stripe_webhook(event_data):
    """
    Process Stripe webhook events
    """
    event_type = event_data.get("type")

    if event_type == "invoice.payment_succeeded":
        handle_successful_payment(event_data["data"]["object"])
    elif event_type == "invoice.payment_failed":
        handle_failed_payment(event_data["data"]["object"])
    elif event_type == "customer.subscription.deleted":
        handle_subscription_cancelled(event_data["data"]["object"])

    logger.info(f"Processed Stripe webhook: {event_type}")


def handle_successful_payment(stripe_invoice):
    """
    Handle successful payment from Stripe
    """
    try:
        invoice = Invoice.objects.get(stripe_invoice_id=stripe_invoice["id"])
        invoice.mark_paid()
        logger.info(f"Marked invoice {invoice.id} as paid")
    except Invoice.DoesNotExist:
        logger.error(f"Invoice not found for Stripe invoice {stripe_invoice['id']}")


def handle_failed_payment(stripe_invoice):
    """
    Handle failed payment from Stripe
    """
    try:
        invoice = Invoice.objects.get(stripe_invoice_id=stripe_invoice["id"])
        invoice.status = "failed"
        invoice.save()
        logger.info(f"Marked invoice {invoice.id} as failed")
    except Invoice.DoesNotExist:
        logger.error(f"Invoice not found for Stripe invoice {stripe_invoice['id']}")


def handle_subscription_cancelled(stripe_subscription):
    """
    Handle subscription cancellation from Stripe
    """
    try:
        subscription = Subscription.objects.get(
            stripe_subscription_id=stripe_subscription["id"]
        )
        subscription.cancel()
        logger.info(f"Cancelled subscription {subscription.id}")
    except Subscription.DoesNotExist:
        logger.error(
            f"Subscription not found for Stripe subscription {stripe_subscription['id']}"
        )
