import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter()
    category = django_filters.CharFilter(lookup_expr='slug')
    genre = django_filters.CharFilter(lookup_expr='slug')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']
