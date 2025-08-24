# reservation/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, BookingViewSet


app_name = 'reservation'

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'bookings', BookingViewSet, basename='booking')


urlpatterns = [
    path('', include(router.urls)),
]
