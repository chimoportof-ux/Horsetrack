from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Horse(models.Model):
    SEX_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
        ('castrado', 'Castrado'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='horses')
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, blank=True)
    current_weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    history = models.TextField(blank=True)
    feeding_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Caballo'
        verbose_name_plural = 'Caballos'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('horse_detail', kwargs={'pk': self.pk})


class HealthRecord(models.Model):
    ISSUE_CHOICES = [
        ('revision', 'Revisión'),
        ('vacuna', 'Vacuna'),
        ('desparasitacion', 'Desparasitación'),
        ('cojera', 'Cojera'),
        ('colico', 'Cólico'),
        ('herida', 'Herida'),
        ('otro', 'Otro'),
    ]

    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='health_records')
    date = models.DateField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    issue_type = models.CharField(max_length=30, choices=ISSUE_CHOICES)
    observations = models.TextField(blank=True)
    veterinarian = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Registro de salud'
        verbose_name_plural = 'Registros de salud'

    def __str__(self):
        return f'{self.horse.name} - {self.date}'


class Training(models.Model):
    TRAINING_TYPES = [
        ('doma', 'Doma'),
        ('paseo', 'Paseo'),
        ('salto', 'Salto'),
        ('cuerda', 'Cuerda'),
        ('campo', 'Campo'),
        ('descanso_activo', 'Descanso activo'),
    ]

    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='trainings')
    date = models.DateField()
    training_type = models.CharField(max_length=30, choices=TRAINING_TYPES)
    duration = models.PositiveIntegerField(help_text='Duración en minutos')
    notes = models.TextField(blank=True)
    intensity = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Entrenamiento'
        verbose_name_plural = 'Entrenamientos'

    def __str__(self):
        return f'{self.horse.name} - {self.training_type} - {self.date}'


class Event(models.Model):
    EVENT_TYPES = [
        ('vacuna', 'Vacuna'),
        ('herrador', 'Herrador'),
        ('desparasitacion', 'Desparasitación'),
        ('veterinario', 'Veterinario'),
        ('revision', 'Revisión general'),
    ]

    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    date = models.DateField()
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f'{self.horse.name} - {self.event_type} - {self.date}'
