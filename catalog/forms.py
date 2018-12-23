import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget

from catalog.models import BookInstance

class RenueBooksForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter the date between 4 weeks (default 3). ", widget=forms.TextInput(attrs=
                                {
                                    'id':'datepicker'
                                }))

    # check if the date is in past
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data

