import django_filters
from django_filters import CharFilter

from .models import Aircraft

class AircraftFilter(django_filters.FilterSet):
    tail_number = CharFilter(field_name='tail_number', lookup_expr='icontains', min_length=2)
    serial_number = CharFilter(field_name='serial_number', lookup_expr='icontains', min_length=2)

    class Meta:
        model = Aircraft
        fields = ['tail_number', 'serial_number']