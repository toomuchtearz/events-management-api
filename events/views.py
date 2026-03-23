from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from events.models import Event
from events.permissions import IsOrganizerOrReadOnly

from events.serializers import (
    EventListSerializer,
    EventRetrieveSerializer
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    permission_classes = (IsAuthenticated, IsOrganizerOrReadOnly)

    def get_queryset(self):
        queryset = Event.objects.select_related(
            "organizer"
        ).prefetch_related("attendees")

        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "list":
            serializer = EventListSerializer
        if self.action == "retrieve":
            serializer = EventRetrieveSerializer

        return serializer
