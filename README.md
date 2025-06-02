# django-rest-saas-demo


# 🧾 SaaS Subscription Billing Backend

This is a backend service for managing user subscriptions, automated invoicing, and payment workflows for a SaaS platform. Built using **Django**, **Celery**, and optional **Stripe** integration.


## 🚀 Features

- 🔐 User registration, login, logout, and profile
- 💳 Plan subscription (Basic, Pro, Enterprise)
- 📆 Automatic monthly invoice generation via Celery
- ⚠️ Overdue invoice detection and payment reminders
- 💰 Mock and Stripe-based payment processing
- 📊 Billing dashboard & admin interface
- ✅ RESTful API design with UUID-based model security

---

## 🧑‍💻 Quick Start (Recommended)

> 💡 **Fastest way to get started:**

Just run:

```bash
sudo docker compose up -d
````

This will:

* Start Django, Celery, RabbitMQ, and Postgres
* Set up environment variables
* Apply migrations
* Seed initial data (plans)
* Expose the API at: `http://localhost:8000`



## 🔗 API Endpoints

### 👤 Authentication

* `POST /api/users/register/`
* `POST /api/users/login/`
* `POST /api/users/logout/`
* `GET  /api/users/profile/`

### 📦 Plans

* `GET /api/billing/plans/`

### 🔁 Subscriptions

* `GET /api/billing/subscriptions/`
* `POST /api/billing/subscribe/`
* `POST /api/billing/subscriptions/{id}/cancel/`

### 💸 Invoices

* `GET /api/billing/invoices/`
* `GET /api/billing/invoices/{id}/`
* `POST /api/billing/invoices/{id}/pay/`
* `POST /api/billing/invoices/{id}/stripe-payment/`

### 📊 Dashboard

* `GET /api/billing/dashboard/`

---

## 🧪 Testing

```bash
# Register a user
curl -X POST http://localhost:8000/api/users/register/ \
-H "Content-Type: application/json" \
-d '{"email": "test@example.com", "username": "testuser", "password": "testpass123", "password_confirm": "testpass123"}'

# Login
curl -X POST http://localhost:8000/api/users/login/ \
-H "Content-Type: application/json" \
-d '{"email": "test@example.com", "password": "testpass123"}'

# List plans
curl -X GET http://localhost:8000/api/billing/plans/
```

