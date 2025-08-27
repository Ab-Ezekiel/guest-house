from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("initialize/", views.initialize_payment_view, name="initialize-payment"),
    path("verify/<str:reference>/", views.verify_payment_view, name="verify-payment"),
]
