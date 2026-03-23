from django.core.mail import send_mail
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from events.filters import EventFilter
from events.models import Event
from events.permissions import IsOrganizerOrReadOnly

from events.serializers import EventListSerializer, EventRetrieveSerializer


def send_event_registration_mail(user, event):
    subject = f"Registration Confirmed: {event.title}"

    message = (
        f"Hi {user.full_name},\n\n"
        f"You are officially registered for {event.title}!\n\n"
        f"Location: {event.location}\n"
        f"Time: {event.time.strftime('%b %d, %Y at %H:%M')}\n\n"
        f"We look forward to seeing you there."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[user.email],
        fail_silently=True,
    )


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    permission_classes = (IsAuthenticated, IsOrganizerOrReadOnly)

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = EventFilter

    search_fields = ("title", "description")
    ordering_fields = ("time", "title")
    ordering = ("-time",)

    def get_queryset(self):
        queryset = Event.objects.select_related("organizer").annotate(
            attendees_count=Count("attendees")
        )

        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        if self.action == "toggle_register":
            return serializers.Serializer
        return EventRetrieveSerializer

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=(IsAuthenticated,),
        url_path="toggle-register",
    )
    def toggle_register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        if event.organizer == user:
            return Response(
                {"detail": "You cannot register for your own event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if event.attendees.filter(id=user.id).exists():
            event.attendees.remove(user)
            return Response(
                {"detail": "Successfully unregistered from the event."},
                status=status.HTTP_200_OK,
            )
        else:
            event.attendees.add(user)
            send_event_registration_mail(user=user, event=event)

            return Response(
                {"detail": "Successfully registered for the event."},
                status=status.HTTP_200_OK,
            )

    @extend_schema(request=None)
    @action(
        detail=False,
        methods=["GET"],
        permission_classes=(IsAuthenticated,)
    )
    def my(self, request):
        my_events = self.get_queryset().filter(organizer=request.user)
        serializer = self.get_serializer(my_events, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=(IsAuthenticated,)
    )
    def attending(self, request):
        attending_events = self.get_queryset().filter(attendees=request.user)
        serializer = self.get_serializer(attending_events, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
