from django import forms
from .models import RegistroFinanciero, Label
from datetime import date
from django_select2.forms import Select2MultipleWidget
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class RegistroFinancieroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        super(RegistroFinancieroForm, self).__init__(*args, **kwargs)
        print(user)
        if user:
            self.fields['label_existente'].queryset = Label.objects.filter(user=user)

    label_existente = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        empty_label="Elige una label existente (opcional)"
    )
    label_personalizada = forms.CharField(
        max_length=255,
        required=False,
        label="O crea una nueva label (opcional)"
    )


    fecha = forms.DateField()


    class Meta:
        model = RegistroFinanciero
        fields = ['tipo', 'monto', 'fecha', 'label_existente', 'label_personalizada', 'nota', 'metodo']
        widgets = {
            'monto': forms.TextInput(attrs={'class': 'rounded-pill'}),
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


    tipo = forms.ChoiceField(
        choices=(('income', 'Ingreso'), ('expense', 'Gasto'),('', 'Todos')),
        required=False,
        label="Tipo de registro",
    )

    metodo = forms.ChoiceField(
        choices=(('cash', 'Efectivo'), ('credit_card', 'Tarjeta'),('', 'Todos')),
        required=False,
        label="Tipo de registro",
        )


class FiltroLabelsListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        super(FiltroLabelsListForm, self).__init__(*args, **kwargs)

    type = forms.ChoiceField(
        choices=(('income', _('Income')), ('expense', _('Expense')),('', _('All'))),
        required=False,
        label=_("Record Type"),
    )

class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': _("Username or Email Address")})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': _("Enter your Password")})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': _("Confirm your Password")})




