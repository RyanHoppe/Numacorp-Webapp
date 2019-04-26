from django import forms
from . models import MaterialsModel, ClockInModel, ClockOutModel
from datetime import datetime


class MaterialsForm(forms.ModelForm):

    class Meta:
        model = MaterialsModel
        fields = ['manager_name', 'materials_used', 'quantity', 'time_submitted']
        

class ClockInForm(forms.ModelForm):

    class Meta:
        model = ClockInModel
        fields = ['employee_name']


class ClockOutForm(forms.ModelForm):

    class Meta:
        model = ClockOutModel
        fields = ['employee_name']


class DateSelectForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.today)