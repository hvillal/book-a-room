from bootstrap_datepicker_plus import DatePickerInput
from django import forms


class DatesSelection(forms.Form):
    check_in = forms.DateField(label='Llegada', required=True, widget=DatePickerInput(format='%d-%m-%Y'))
    check_out = forms.DateField(label='Salida', required=True, widget=DatePickerInput(format='%d-%m-%Y'))
