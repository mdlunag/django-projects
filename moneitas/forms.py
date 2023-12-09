from django import forms
from .models import FinancialRecord, Label, METHOD_CHOICES
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


    date = forms.DateField()


    class Meta:
        model = FinancialRecord
        fields = ['type', 'amount', 'date', 'label_existente', 'label_personalizada', 'comment', 'method']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'rounded-pill'}),
        }


class FiltroDashboardForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        super(FiltroDashboardForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['labels'].queryset = Label.objects.filter(user=user)

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
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




