from django import forms
from .models import FinancialRecord, Label, RecurrentRecord, METHOD_CHOICES, CADENCE_CHOICES
from datetime import date
from django_select2.forms import Select2MultipleWidget
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

TYPE_CHOICES = (('income', _('Income')), ('expense', _('Expense')),('', _('All')))
METHOD_CHOICES += ('', _('All')),

class FinancialRecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        super(FinancialRecordForm, self).__init__(*args, **kwargs)
        print(user)
        if user:
            self.fields['label_existente'].queryset = Label.objects.filter(user=user)

    label_existente = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        empty_label=_("Choose existing label (optional)")
    )
    label_personalizada = forms.CharField(
        max_length=255,
        required=False,
        label="O crea una nueva etiqueta (opcional)"
    )

    income_paid = forms.BooleanField(required=False,initial=False,widget=forms.CheckboxInput(attrs={'class': "form-check-input ms-1"}))

    date = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d", 
            attrs={"type": "date"}),
            input_formats=["%Y-%m-%d"])

    class Meta:
        model = FinancialRecord
        fields = ['type', 'amount', 'date', 'label_existente', 'label_personalizada', 'comment', 'method', 'income_paid']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'rounded-pill'}),
        }


class FiltroDashboardForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        type_selected = kwargs.pop('type_labels')
        super(FiltroDashboardForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['labels'].queryset = Label.objects.filter(user=user).order_by('name')
        if type_selected:
            self.fields['labels'].queryset = Label.objects.filter(user=user, type=type_selected).order_by('name')

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all().order_by('name'),
        required=False,
        widget=Select2MultipleWidget()
    )


    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=False,
        label="Tipo de registro",
    )

    method = forms.ChoiceField(
        choices=METHOD_CHOICES,
        required=False,
        label="Tipo de registro",
        )


class FiltroLabelsListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        super(FiltroLabelsListForm, self).__init__(*args, **kwargs)

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=False,
        label=_("Record Type"),
    )

class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': _("Username or Email Address")})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': _("Enter your Password")})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': _("Confirm your Password")})

class FiltroRecurrentRecordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        super(FiltroRecurrentRecordForm, self).__init__(*args, **kwargs)

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=False,
        label=_("Record Type"),
    )

    cadence_type = forms.ChoiceField(
        choices=CADENCE_CHOICES,
        required=False,
        label=_('Cadence')
    )

class RecurrentRecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        super(RecurrentRecordForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['label_existente'].queryset = Label.objects.filter(user=user)

    label_existente = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        empty_label=_("Choose existing label (optional)")
    )
    label_personalizada = forms.CharField(
        max_length=255,
        required=False,
        label="O crea una nueva etiqueta (opcional)"
    )

    date_from = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d", 
            attrs={"type": "date"}),
            input_formats=["%Y-%m-%d"])

    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format="%Y-%m-%d", 
            attrs={"type": "date"}),
            input_formats=["%Y-%m-%d"])
    
    cadence_position = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'min': 1, 'required': True}),
    )

    def clean(self):
        cleaned_data = super().clean()
        cadence_type = cleaned_data.get('cadence_type')
        cadence_position = cleaned_data.get('cadence_position')
        if cadence_type == 'weekly' and (cadence_position < 1 or cadence_position > 7):
            raise forms.ValidationError(
                "For weekly cadence, cadence position must be between 1 and 7."
            )

        elif cadence_type == "monthly" and cadence_position > 31:
            raise forms.ValidationError(
                "For monthly cadence, cadence position must be between 1 and 31."
            )

        return cleaned_data

    class Meta:
        model = RecurrentRecord
        fields = ['comment', 'type', 'amount', 'date_from', 'date_to', 'label_existente', 'label_personalizada', 'method', 'cadence_type', 'cadence_position']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'rounded-pill'}),
        }
