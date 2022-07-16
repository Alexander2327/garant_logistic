from django_filters.rest_framework import FilterSet, NumberFilter, RangeFilter, CharFilter

from .models import Table


class TableFilter(FilterSet):
    number_of_seats = NumberFilter(field_name='number_of_seats')
    price = RangeFilter(field_name='price')

    class Meta:
        model = Table
        fields = ('number_of_seats', 'price', 'type_id')
