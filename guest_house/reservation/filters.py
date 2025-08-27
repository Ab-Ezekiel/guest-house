# reservation/filters.py
import django_filters as filters
from .models import Room

class RoomFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    type = filters.CharFilter(field_name="type", lookup_expr="iexact")
    is_available = filters.BooleanFilter(field_name="is_available")

    class Meta:
        model = Room
        fields = ["type", "is_available", "min_price", "max_price"]

