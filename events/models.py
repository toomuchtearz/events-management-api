from django.conf import settings
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    time = models.DateTimeField()
    location = models.CharField(max_length=64)

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="events",
        on_delete=models.CASCADE
    )
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="attended_events",
        blank=True
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-time"]
