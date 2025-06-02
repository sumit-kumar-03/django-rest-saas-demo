from celery.schedules import crontab
from app.celery.celery import saas_project_celery_app
from app.billing.tasks import (
    mark_overdue_invoices,
    send_payment_reminders,
    generate_invoices_for_active_subscriptions,
)


@saas_project_celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(hour=1, minute=0),
        mark_overdue_invoices.s("Runs every day at 1 AM and marks overdue invoices"),
    ),

    sender.add_periodic_task(
        crontab(hour=10, minute=0),
        send_payment_reminders.s("Runs every day at 10 AM and sends payment reminders"),
    ),

    sender.add_periodic_task(
        crontab(hour=9, minute=0),
        generate_invoices_for_active_subscriptions.s(
            "Runs every day at 9 AM and generates invoices for active subscriptions"
        ),
    ),
