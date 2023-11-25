from django import forms
from .models import RegistroFinanciero, Etiqueta
from datetime import date
from django_select2.forms import Select2MultipleWidget

class RegistroFinancieroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        super(RegistroFinancieroForm, self).__init__(*args, **kwargs)
        print(user)
        if user:
            self.fields['etiqueta_existente'].queryset = Etiqueta.objects.filter(user=user)

    etiqueta_existente = forms.ModelChoiceField(
        queryset=Etiqueta.objects.all(),
        required=False,
        empty_label="Elige una etiqueta existente (opcional)"
    )
    etiqueta_personalizada = forms.CharField(
        max_length=255,
        required=False,
        label="O crea una nueva etiqueta (opcional)"
    )


    fecha = forms.DateField()


    class Meta:
        model = RegistroFinanciero
        fields = ['tipo', 'monto', 'fecha', 'etiqueta_existente', 'etiqueta_personalizada', 'nota', 'metodo']
        widgets = {
            'monto': forms.TextInput(attrs={'class': 'rounded-pill'}),
        }


class FiltroDashboardForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        super(FiltroDashboardForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['etiquetas'].queryset = Etiqueta.objects.filter(user=user)

    etiquetas = forms.ModelMultipleChoiceField(
        queryset=Etiqueta.objects.all(),
        required=False,
        widget=Select2MultipleWidget()
    )


    tipo = forms.ChoiceField(
        choices=(('ingreso', 'Ingreso'), ('gasto', 'Gasto'),('', 'Todos')),
        required=False,
        label="Tipo de registro",
    )

    metodo = forms.ChoiceField(
        choices=(('cash', 'Efectivo'), ('credit_card', 'Tarjeta'),('', 'Todos')),
        required=False,
        label="Tipo de registro",
        )


class FiltroEtiquetasListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario de los argumentos
        super(FiltroEtiquetasListForm, self).__init__(*args, **kwargs)

    tipo = forms.ChoiceField(
        choices=(('ingreso', 'Ingreso'), ('gasto', 'Gasto'),('', 'Todos')),
        required=False,
        label="Tipo de registro",
    )




