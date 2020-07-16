import django_filters
from django_filters import DateFilter
from .models import *

class order_filter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='lte')
    end_date = DateFilter(field_name="date_created", lookup_expr='gte')
    class Meta:
        model=order_model
        fields=['products_mod','status']
        

