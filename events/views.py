from django.db.models import Count
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        queryset = Event.objects.select_related("organizer").annotate(
            attendees_count=Count("attendees")
        )

        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "list":
            serializer = EventListSerializer
        return serializer

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=(IsAuthenticated,),
        serializer_class=serializers.Serializer,
        url_path="toggle-register"
    )
    def toggle_register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        if event.attendees.filter(id=user.id).exists():
            event.attendees.remove(user)
            return Response({"detail": "Successfully unregistered from the event."}, status=status.HTTP_200_OK)
        else:
            event.attendees.add(user)
            return Response({"detail": "Successfully registered for the event."}, status=status.HTTP_200_OK)


    @action(detail=False, methods=["GET"], permission_classes=(IsAuthenticated,))
    def my(self, request):
        my_events = self.get_queryset().filter(organizer=request.user)
        serializer = self.get_serializer(my_events, many=True)

        return Response(serializer.data)


    @action(detail=False, methods=["GET"], permission_classes=(IsAuthenticated,))
    def attending(self, request):
        attending_events = self.get_queryset().filter(attendees=request.user)
        serializer = self.get_serializer(attending_events, many=True)

        return Response(serializer.data)
