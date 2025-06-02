from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(
        "users/",
        include("app.users.urls"),
    ),
    path(
        "billing/",
        include("app.billing.urls"),
    ),
]
