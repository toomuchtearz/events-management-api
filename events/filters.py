from django_filters import rest_framework as filters
from events.models import Event


class EventFilter(filters.FilterSet):
    location = filters.CharFilter(lookup_expr="icontains")

    time_after = filters.IsoDateTimeFilter(
        field_name="time",
        lookup_expr="gte"
    )
    time_before = filters.IsoDateTimeFilter(
        field_name="time",
        lookup_expr="lte"
    )

    class Meta:
        model = Event
        fields = ["location", "time_after", "time_before"]
