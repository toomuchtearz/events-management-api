from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase
from events.models import Event

User = get_user_model()


class EventApiTests(APITestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            email="organizer@test.com",
            password="password123",
            first_name="John",
            last_name="Cena"
        )
        self.participant = User.objects.create_user(
            email="user@test.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )

        self.event = Event.objects.create(
            title="Django Workshop",
            description="Learn DRF",
            time="2026-05-01T10:00:00Z",
            location="Kyiv",
            organizer=self.organizer
        )

        self.list_url = reverse("events:events-list")
        self.detail_url = reverse("events:events-detail", args=[self.event.id])
        self.register_url = reverse("events:events-toggle-register", args=[self.event.id])


    def test_anonymous_user_cannot_access_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_organizer_cannot_update_event(self):
        self.client.force_authenticate(user=self.participant)
        payload = {"title": "Hacked Title"}
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_event_sets_organizer(self):
        self.client.force_authenticate(user=self.organizer)
        payload = {
            "title": "New Event",
            "description": "Test Desc",
            "time": "2026-06-01T12:00:00Z",
            "location": "Lviv"
        }
        response = self.client.post(self.list_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["organizer"], self.organizer.full_name)

    def test_list_contains_annotated_fields(self):
        self.client.force_authenticate(user=self.participant)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attendees_count", response.data[0])
        self.assertEqual(response.data[0]["organizer"], self.organizer.full_name)


    def test_organizer_cannot_register_for_own_event(self):
        self.client.force_authenticate(user=self.organizer)
        response = self.client.post(self.register_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "You cannot register for your own event.")

    def test_successful_registration_and_email(self):
        self.client.force_authenticate(user=self.participant)
        response = self.client.post(self.register_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.event.attendees.filter(id=self.participant.id).exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Registration Confirmed", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, [self.participant.email])

    def test_successful_unregistration(self):
        self.event.attendees.add(self.participant)
        self.client.force_authenticate(user=self.participant)

        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.event.attendees.filter(id=self.participant.id).exists())
        self.assertEqual(response.data["detail"], "Successfully unregistered from the event.")


    def test_my_events_action(self):
        self.client.force_authenticate(user=self.organizer)
        url = reverse("events:events-my")
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.event.title)

    def test_attending_events_action(self):
        self.event.attendees.add(self.participant)
        self.client.force_authenticate(user=self.participant)
        url = reverse("events:events-attending")
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.event.title)