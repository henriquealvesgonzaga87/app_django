from django.contrib import admin
from core.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_date", "event_creation_date")
    list_filter = ("user", "event_date",)


admin.site.register(Event, EventAdmin)
