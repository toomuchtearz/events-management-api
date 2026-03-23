from rest_framework import serializers

from events.models import Event


class EventListSerializer(serializers.ModelSerializer):
    attendees_count = serializers.IntegerField(read_only=True)
    organizer = serializers.CharField(
        source="organizer.full_name",
        read_only=True
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "time",
            "location",
            "organizer",
            "attendees_count",
        )
        read_only_fields = ("organizer",)


class EventRetrieveSerializer(serializers.ModelSerializer):
    attendees_count = serializers.IntegerField(read_only=True)
    organizer = serializers.CharField(
        source="organizer.full_name",
        read_only=True
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "time",
            "location",
            "description",
            "organizer",
            "attendees_count",
        )
        read_only_fields = ("organizer",)


class EventToggleSerializer(serializers.Serializer):
    """Empty serializer for the toggle_register action."""
    pass
