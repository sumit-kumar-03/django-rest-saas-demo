# django-rest-saas-demo


## SETUP INSTRUCTIONS:

1. Create virtual environment:
   python -m venv venv
   source venv/bin/activate 

2. Install dependencies:
   pip install -r requirements.txt

3. Create .env file with your configuration:
   ```DEBUG=True
   SECRET_KEY=your-secret-key-here
   STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
   ```

4. Run migrations:
   python manage.py makemigrations app
   python manage.py migrate

5. Create superuser:
   python manage.py createsuperuser

6. Load initial data (plans):
   ```python manage.py shell
   >>> from app.billing.models import Plan
   >>> Plan.objects.create(name="Basic", plan_type="basic", price=9.99, features=["Feature 1", "Feature 2"])
   >>> Plan.objects.create(name="Pro", plan_type="pro", price=19.99, features=["All Basic features", "Feature 3", "Feature 4"])
   >>> Plan.objects.create(name="Enterprise", plan_type="enterprise", price=49.99, features=["All Pro features", "Feature 5", "Premium support"])
   ```

7. Start RabbitMQ server:

8. Start Celery worker:

9. Start Celery beat (scheduler):

10. Run Django server:
    python manage.py runserver

## API ENDPOINTS:

### Authentication:
- POST /api/users/register/ - Register new user
- POST /api/users/login/ - Login user
- POST /api/users/logout/ - Logout user
- GET /api/users/profile/ - Get user profile

### Plans:
- GET /api/billing/plans/ - List all plans

### Subscriptions:
- GET /api/billing/subscriptions/ - List user subscriptions
- POST /api/billing/subscribe/ - Subscribe to plan
- POST /api/billing/subscriptions/{id}/cancel/ - Cancel subscription

### Invoices:
- GET /api/billing/invoices/ - List user invoices
- GET /api/billing/invoices/{id}/ - Get invoice details
- POST /api/billing/invoices/{id}/pay/ - Pay invoice (mock)
- POST /api/billing/invoices/{id}/stripe-payment/ - Create Stripe payment intent

### Dashboard:
- GET /api/billing/dashboard/ - Get billing dashboard data

## TESTING:

1. Register a user:
   curl -X POST http://localhost:8000/api/users/register/ \
   -H "Content-Type: application/json" \
   -d '{"email": "test@example.com", "username": "testuser", "password": "testpass123", "password_confirm": "testpass123"}'

2. Login:
   curl -X POST http://localhost:8000/api/users/login/ \
   -H "Content-Type: application/json" \
   -d '{"email": "test@example.com", "password": "testpass123"}'

3. Get plans:
   curl -X GET http://localhost:8000/api/billing/plans/

4. Subscribe to plan:
   curl -X POST http://localhost:8000/api/billing/subscribe/ \
   -H "Content-Type: application/json" \
   -H "Cookie: sessionid=your-session-id" \
   -d '{"plan": "plan-uuid-here"}'

## CELERY TASKS:

The following tasks run automatically:
- generate_invoices_for_active_subscriptions: Daily at midnight
- mark_overdue_invoices: Daily at 1 AM
- send_payment_reminders: Daily at 9 AM

You can also run tasks manually:
celery -A subscription_billing call billing.tasks.generate_invoices_for_active_subscriptions
celery -A subscription_billing call billing.tasks.mark_overdue_invoices
celery -A subscription_billing call billing.tasks.send_payment_reminders

## FEATURES IMPLEMENTED:

- ✅ User authentication and management
- ✅ Plan management (Basic, Pro, Enterprise)
- ✅ Subscription lifecycle (subscribe, cancel, expire)
- ✅ Automatic invoice generation with Celery
- ✅ Payment processing (mock and Stripe integration)
- ✅ Overdue invoice detection
- ✅ Payment reminder system
- ✅ REST API endpoints
- ✅ Admin interface
- ✅ Billing dashboard
- ✅ Webhook handling for Stripe events
- ✅ Comprehensive error handling
- ✅ Logging and monitoring

## BONUS FEATURES:
- ✅ Email reminders (mock implementation)
- ✅ Stripe integration for real payments
- ✅ Webhook handling for payment events
- ✅ Dashboard with billing overview
- ✅ UUID-based model IDs for security
- ✅ Comprehensive admin interface