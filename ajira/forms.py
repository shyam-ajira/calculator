# ajira/forms.py

from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_type', 'quantity', 'flooring_type')

RoomFormSet = forms.formset_factory(RoomForm, extra=0)