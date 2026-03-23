from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from events.models import Event
from events.permissions import IsOrganizerOrReadOnly

from events.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, IsOrganizerOrReadOnly)

    def get_queryset(self):
        queryset = Event.objects.select_related(
            "organizer"
        ).prefetch_related("attendees")

        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
