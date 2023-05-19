from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField(verbose_name="Event date")
    event_creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'event'

    def __str__(self):
        return f"event: {self.title} - on {self.event_date}"

    def get_data_event(self):
        return self.event_date.strftime("%d/%m/%Y %H:%M")

    def get_date_input_event(self):
        return self.event_date.strftime("%Y-%m-%dT%H:%M")

