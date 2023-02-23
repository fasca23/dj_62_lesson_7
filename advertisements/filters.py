from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = filters.DateFromToRangeFilter()
    # TODO: задайте требуемые фильтры

    class Meta:
        model = Advertisement
        fields = ['title', 'creator', 'created_at', 'status']
