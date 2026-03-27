from django.urls import path
from . import views

from .views import (
    HorseCreateView,
    HorseDeleteView,
    HorseDetailView,
    HorseListView,
    HorseUpdateView,
    create_event,
    create_health_record,
    create_training,
    dashboard,
    event_list,
    health_list,
    register,
    training_list,
    CalendarView,
    CalendarEventsJsonView
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('horses/', HorseListView.as_view(), name='horse_list'),
    path('horses/new/', HorseCreateView.as_view(), name='horse_create'),
    path('horses/<int:pk>/', HorseDetailView.as_view(), name='horse_detail'),
    path('horses/<int:pk>/edit/', HorseUpdateView.as_view(), name='horse_update'),
    path('horses/<int:pk>/delete/', HorseDeleteView.as_view(), name='horse_delete'),
    path('health/', health_list, name='health_list'),
    path('health/new/', create_health_record, name='health_create'),
    path('trainings/', training_list, name='training_list'),
    path('trainings/new/', create_training, name='training_create'),
    path('events/', event_list, name='event_list'),
    path('events/new/', create_event, name='event_create'),
    path('events/<int:pk>/toggle-completed/', views.EventToggleCompletedView.as_view(), name='event_toggle_completed'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('calendar/events/', CalendarEventsJsonView.as_view(), name='calendar_events_json'),
]
