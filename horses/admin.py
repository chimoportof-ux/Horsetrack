from django.contrib import admin

from .models import Event, HealthRecord, Horse, Training


@admin.register(Horse)
class HorseAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'owner', 'current_weight')
    search_fields = ('name', 'breed', 'owner__username')
    list_filter = ('breed', 'sex')


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('horse', 'date', 'issue_type', 'weight', 'veterinarian')
    list_filter = ('issue_type', 'date')
    search_fields = ('horse__name', 'observations', 'veterinarian')


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('horse', 'date', 'training_type', 'duration', 'intensity')
    list_filter = ('training_type', 'date')
    search_fields = ('horse__name', 'notes', 'intensity')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('horse', 'event_type', 'date', 'completed')
    list_filter = ('event_type', 'completed', 'date')
    search_fields = ('horse__name', 'description')
