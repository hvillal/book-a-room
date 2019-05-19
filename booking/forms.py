from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ('number', 'room', 'created', 'guest', 'check_in', 'check_out', 'total')
        widgets = {
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0000 0000 0000 0000'
            }),
            'expiry_month': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'MM'
            }),
            'expiry_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'AA'
            }),
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.number = kwargs.pop('number', None)
        self.room = kwargs.pop('room', None)
        self.guest = kwargs.pop('guest', None)
        self.check_in = kwargs.pop('check_in', None)
        self.check_out = kwargs.pop('check_out', None)
        self.total = kwargs.pop('total', None)
        super(ReservationForm, self).__init__(*args, **kwargs)
