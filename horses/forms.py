from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Event, HealthRecord, Horse, Training


class DateInput(forms.DateInput):
    input_type = 'date'


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class HorseForm(forms.ModelForm):
    class Meta:
        model = Horse
        fields = ['name', 'age', 'breed', 'sex', 'current_weight', 'history', 'feeding_notes']


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['horse', 'date', 'weight', 'issue_type', 'observations', 'veterinarian']
        widgets = {'date': DateInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['horse'].queryset = Horse.objects.filter(owner=user)


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['horse', 'date', 'training_type', 'duration', 'intensity', 'notes']
        widgets = {'date': DateInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['horse'].queryset = Horse.objects.filter(owner=user)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['horse', 'event_type', 'date', 'description', 'completed']
        widgets = {'date': DateInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['horse'].queryset = Horse.objects.filter(owner=user)
