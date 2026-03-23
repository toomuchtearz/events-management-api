from rest_framework import serializers

from events.models import Event


class EventListSerializer(serializers.ModelSerializer):
    attendees_count = serializers.IntegerField(read_only=True)

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


class EventRetrieveSerializer(serializers.ModelSerializer):
    attendees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "time",
            "location",
            "description",
            "organizer",
            "attendees_count"
        )
