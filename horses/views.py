from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse

from .forms import EventForm, HealthRecordForm, HorseForm, RegisterForm, TrainingForm
from .models import Event, HealthRecord, Horse, Training


class OwnerQuerySetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class HorseListView(OwnerQuerySetMixin, ListView):
    model = Horse
    template_name = 'horses/horse_list.html'
    context_object_name = 'horses'


class HorseDetailView(OwnerQuerySetMixin, DetailView):
    model = Horse
    template_name = 'horses/horse_detail.html'
    context_object_name = 'horse'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horse = self.object

        import json
        from django.db.models import Count, Sum
        from django.db.models.functions import TruncWeek

        # 1. Evolución del peso
        health_records = horse.health_records.order_by('date')
        weight_dates = [record.date.strftime('%Y-%m-%d') for record in health_records]
        weight_values = [float(record.weight) for record in health_records]

        # 2. Minutos entrenados por semana
        trainings_by_week = (
            horse.trainings
            .annotate(week=TruncWeek('date'))
            .values('week')
            .annotate(total_minutes=Sum('duration'))
            .order_by('week')
        )

        week_labels = [
            item['week'].strftime('%Y-%m-%d') if item['week'] else ''
            for item in trainings_by_week
        ]
        week_minutes = [item['total_minutes'] or 0 for item in trainings_by_week]

        # 3. Tipos de entrenamiento
        trainings_by_type = (
            horse.trainings
            .values('training_type')
            .annotate(total=Count('id'))
            .order_by('training_type')
        )

        type_labels = [item['training_type'] for item in trainings_by_type]
        type_counts = [item['total'] for item in trainings_by_type]

        context['weight_dates'] = json.dumps(weight_dates)
        context['weight_values'] = json.dumps(weight_values)

        context['week_labels'] = json.dumps(week_labels)
        context['week_minutes'] = json.dumps(week_minutes)

        context['type_labels'] = json.dumps(type_labels)
        context['type_counts'] = json.dumps(type_counts)

        return context


class HorseCreateView(LoginRequiredMixin, CreateView):
    model = Horse
    form_class = HorseForm
    template_name = 'horses/form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Caballo creado correctamente.')
        return super().form_valid(form)


class HorseUpdateView(OwnerQuerySetMixin, UpdateView):
    model = Horse
    form_class = HorseForm
    template_name = 'horses/form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Caballo actualizado correctamente.')
        return super().form_valid(form)


class HorseDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Horse
    template_name = 'horses/confirm_delete.html'
    success_url = reverse_lazy('horse_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Caballo eliminado correctamente.')
        return super().delete(request, *args, **kwargs)


@login_required
def dashboard(request):
    horses = Horse.objects.filter(owner=request.user)
    upcoming_events = Event.objects.filter(horse__owner=request.user, completed=False, date__gte=timezone.localdate()).order_by('date')[:5]
    recent_trainings = Training.objects.filter(horse__owner=request.user).select_related('horse')[:5]
    recent_health_records = HealthRecord.objects.filter(horse__owner=request.user).select_related('horse')[:5]
    stats = {
        'horse_count': horses.count(),
        'training_count': Training.objects.filter(horse__owner=request.user).count(),
        'health_count': HealthRecord.objects.filter(horse__owner=request.user).count(),
        'pending_events': Event.objects.filter(horse__owner=request.user, completed=False).count(),
    }
    return render(request, 'horses/dashboard.html', {
        'horses': horses[:5],
        'upcoming_events': upcoming_events,
        'recent_trainings': recent_trainings,
        'recent_health_records': recent_health_records,
        'stats': stats,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def health_list(request):
    records = HealthRecord.objects.filter(horse__owner=request.user).select_related('horse')
    return render(request, 'horses/health_list.html', {'records': records})


@login_required
def training_list(request):
    trainings = Training.objects.filter(horse__owner=request.user).select_related('horse')
    return render(request, 'horses/training_list.html', {'trainings': trainings})


@login_required
def event_list(request):
    events = Event.objects.filter(horse__owner=request.user).select_related('horse')
    return render(request, 'horses/event_list.html', {'events': events})


@login_required
def create_health_record(request):
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, user=request.user)
        if form.is_valid():
            record = form.save()
            record.horse.current_weight = record.weight
            record.horse.save(update_fields=['current_weight'])
            messages.success(request, 'Registro de salud guardado correctamente.')
            return redirect('health_list')
    else:
        form = HealthRecordForm(user=request.user)
    return render(request, 'horses/form.html', {'form': form, 'title': 'Nuevo registro de salud'})


@login_required
def create_training(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrenamiento guardado correctamente.')
            return redirect('training_list')
    else:
        form = TrainingForm(user=request.user)
    return render(request, 'horses/form.html', {'form': form, 'title': 'Nuevo entrenamiento'})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento guardado correctamente.')
            return redirect('event_list')
    else:
        form = EventForm(user=request.user)
    return render(request, 'horses/form.html', {'form': form, 'title': 'Nuevo evento'})

class EventToggleCompletedView(OwnerQuerySetMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(
            Event.objects.filter(horse__owner=request.user),
            pk=pk
        )

        event.completed = 'completed' in request.POST
        event.save()

        messages.success(request, 'Estado del evento actualizado.')
        return redirect('event_list')

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'calendar/calendar.html'


class CalendarEventsJsonView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        events_data = []

        horses = Horse.objects.filter(owner=request.user)

        for event in Event.objects.filter(horse__in=horses):
            events_data.append({
                'title': f'Evento - {event.horse.name} ({event.get_event_type_display()})',
                'start': event.date.strftime('%Y-%m-%d'),
                'color': '#dc3545',
                'url': reverse_lazy('event_list'),
            })

        for training in Training.objects.filter(horse__in=horses):
            events_data.append({
                'title': f'Entrenamiento - {training.horse.name} ({training.get_training_type_display()})',
                'start': training.date.strftime('%Y-%m-%d'),
                'color': '#0d6efd',
                'url': reverse_lazy('training_list'),
            })

        for record in HealthRecord.objects.filter(horse__in=horses):
            events_data.append({
                'title': f'Salud - {record.horse.name} ({record.weight} kg)',
                'start': record.date.strftime('%Y-%m-%d'),
                'color': '#198754',
                'url': reverse_lazy('health_list'),
            })

        return JsonResponse(events_data, safe=False)