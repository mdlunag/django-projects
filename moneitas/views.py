from .models import FinancialRecord, Task, Label
from .forms import FinancialRecordForm, FiltroDashboardForm, FiltroLabelsListForm, UserCreationForm

from calendar import month_name
from datetime import date, timedelta

from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

#Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer


#To Do list
def todo(request):
    tasks_todo = Task.objects.filter(state='incomplete')
    tasks_done = Task.objects.filter(state='complete')
    if request.method == 'POST':
        name = request.POST.get('name')
        task = Task(name=name, state="INCOMPLETE")
        task.save()
        # Procesar el formulario de eliminación
        for task in Task.objects.all():
            if request.POST.get(f"delete_{task.id}") == 'on':
                task.delete()
        return redirect('todo')

    return render(request, 'moneitas/to_do.html', {
        'tasks_todo': tasks_todo,
        'tasks_done': tasks_done,
        'todo_disabled': True,
        },)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Aplica la verificación de autenticación solo a esta función
def create_task(request):
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  # Aplica la verificación de autenticación solo a esta función
def edit_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'La tarea no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = TaskSerializer(task, data=request.data,partial=True)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'La tarea no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Tarea eliminada exitosamente'}, status=status.HTTP_204_NO_CONTENT)


#Etiquetas
@login_required
def get_labels(request):
    type = request.GET.get('type')
    labels = Label.objects.filter(type=type)
    if request.user.username != 'admin':
        labels = labels.filter(user=request.user)
    print(labels)
    return JsonResponse({'labels': list(labels.values('id', 'name'))})

@login_required
def list_labels(request):
    labels = Label.objects.filter(user=request.user)
    if request.method == 'POST':
        # Procesar el formulario de eliminación
        for label in labels:
            if request.POST.get(f"delete_{label.id}") == 'on':
                label.delete()
        return redirect('list_labels')

    # Procesar el formulario de filtro
    filter_form = FiltroLabelsListForm(request.GET, user=request.user)

    if filter_form.is_valid():
        selected_type = filter_form.cleaned_data.get('type')

        if selected_type and selected_type != '':
            labels = labels.filter(type=selected_type)

    return render(request, 'moneitas/labels.html', {
        'labels': labels,
        'labels_disabled': True,
        'filter_form': filter_form,
        },)

@login_required
def create_label(request, edit=None):
    if request.method == 'POST':

        type = request.POST.get('type')
        name = request.POST.get('name')

        label = Label(name=name, type=type) if not edit else Label.objects.get(id=edit)

        # Asigna el valor del campo type según la selección del botón de alternancia.
        label.type = type
        label.name = name
        label.user = request.user

        #label.user= User.objects.get(username='aitor.rife@gmail.com')
        #label.user = request.user

        label.save()

        # Redirige al usuario a la página del panel de control con el filtro aplicado
        return redirect(reverse('list_labels'))

    if edit:
        label_edit = Label.objects.get(id=edit)

        return render(request, 'moneitas/create_label.html', {
            'type': label_edit.type,
            'name': label_edit.name,
            })


    return render(request, 'moneitas/create_label.html')

#Login/SignIn
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Intenta crear el usuario
            try:
                user = form.save()
                messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
                return redirect('login')  # Redirige al usuario a la página de inicio de sesión
            except Exception as e:
                messages.error(request, f'Error al registrar: {str(e)}')  # Muestra un mensaje de error
        else:
            errors = form.errors  # Obtiene todos los errores del formulario
    else:
        form = UserCreationForm()

    return render(request, 'moneitas/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('overview_dashboard')
    return render(request, 'moneitas/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

#Registro Financiero
@login_required
def create_financial_record(request, edit=None):
    if request.method == 'POST':
        form = FinancialRecordForm(request.POST, user=request.user)
        if form.is_valid():
            record = form.save(commit=False) if not edit else FinancialRecord.objects.get(id=edit)
            etiqueta_existente = form.cleaned_data['label_existente']
            etiqueta_personalizada = form.cleaned_data['label_personalizada']

            # Verifica si se seleccionó una etiqueta existente o se proporcionó una etiqueta personalizada.
            if etiqueta_existente:
                etiqueta = etiqueta_existente
            elif etiqueta_personalizada:
                # Crea una nueva etiqueta personalizada.
                etiqueta = Label.objects.create(name=etiqueta_personalizada, user=request.user, type=record.type or request.POST.get('type'))
            else:
                # Maneja el caso en el que no se proporciona ninguna etiqueta.
                etiqueta = None
            # Asigna el valor del campo type según la selección del botón de alternancia.
            type = request.POST.get('type')
            comment = request.POST.get('comment')
            method = request.POST.get('method')
	        # Crea el registro financiero con la etiqueta asociada.
            record.label = etiqueta  # Asocia la etiqueta con el record financiero
            record.type = type
            record.comment = comment or ''
            record.method = method
            #registro.user= User.objects.get(username='aitor.rife@gmail.com')
            record.user = request.user
            if edit:
                record.amount = form.cleaned_data['amount']
                record.date = form.cleaned_data['date']
                record.comment = form.cleaned_data['comment']

            record.save()

             # Después de crear el registro, obtén el mes del registro creado
            month_record = record.date.month  # Asegúrate de reemplazar "nuevo_registro" con la variable real que contiene el registro recién creado


            # Construye la URL de redirección con el parámetro "month" del mes del registro
            url_redireccion = reverse('overview_dashboard') + f'?month={month_record}'

            # Redirige al usuario a la página del panel de control con el filtro aplicado
            return redirect(url_redireccion)
    if edit:
        record_edit = FinancialRecord.objects.get(id=edit)
        print(record_edit.type)
        form = FinancialRecordForm(initial={
            'type': 'income' if record_edit.type == 'income' else 'expense',
            'method': record_edit.method,
            'amount': record_edit.amount,
            'date': record_edit.date,
            'label_existente': record_edit.label or '',
            'comment':  record_edit.comment,

            })
    else:
        form = FinancialRecordForm(initial={'date': date.today(), 'comment':''}, user=request.user)  # Prellenar la fecha con la fecha actual

    return render(request, 'moneitas/create_financial_record.html', {'form': form})

from django.db.models import Q


def filtrar_registros(financial_records, etiqueta, type):
    # Construye una consulta de filtro dinámica
    filtro = Q()  # Query vacía inicialmente

    if etiqueta:
        filtro &= Q(etiqueta=etiqueta)

    if type:
        filtro &= Q(type=type)

    # Aplica el filtro a los registros financieros
    return financial_records.filter(filtro)

@login_required
def overview_dashboard(request):
    # Obtener la fecha actual
    current_date = date.today()

    # Obtener el mes seleccionado del parámetro GET, si está presente
    selected_month = request.GET.get('month', current_date.month)

    # Calcular el primer y último día del mes seleccionado (si no es "Todos")
    if selected_month != 'Todos':
        selected_month = int(selected_month)
        first_day_of_month = current_date.replace(month=selected_month, day=1)
        last_day_of_month = first_day_of_month.replace(
            month=first_day_of_month.month % 12 + 1,
            year=first_day_of_month.year + first_day_of_month.month // 12,
            day=1
        ) - timedelta(days=1)
    else:
        first_day_of_month = None
        last_day_of_month = None

    # Obtener una lista de meses con datos
    months_with_data = FinancialRecord.objects.filter(
        date__year=current_date.year
    ).dates('date', 'month')

    # Convertir los objetos de fecha a names de mes legibles
    month_choices = [(month.month, month_name[month.month]) for month in months_with_data]
    month_choices += [('Todos', 'Todos')]

    # Filtrar registros financieros según el rango de fechas (si no es "Todos")
    if first_day_of_month and last_day_of_month:
        financial_records = FinancialRecord.objects.filter(
            date__range=[first_day_of_month, last_day_of_month]
        )
    else:
        financial_records = FinancialRecord.objects.all()

    # Procesar el formulario de filtro
    filter_form = FiltroDashboardForm(request.GET, user=request.user)

    if filter_form.is_valid():
        selected_labels = filter_form.cleaned_data.get('labels')
        type_seleccionado = filter_form.cleaned_data.get('type')
        method_seleccionado = filter_form.cleaned_data.get('method')

        if method_seleccionado and method_seleccionado != '':
            financial_records = financial_records.filter(method=method_seleccionado)

        if selected_labels:
            financial_records = financial_records.filter(label__in=selected_labels)

        if type_seleccionado and type_seleccionado != '':
            financial_records = financial_records.filter(type=type_seleccionado)

    if request.user.username != 'admin':
        financial_records = financial_records.filter(user=request.user)

    incomes = financial_records.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = financial_records.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

    # Calcular el saldo total
    balance = incomes - expenses

    if request.method == 'POST':
        # Procesar el formulario de eliminación
        for registro in financial_records:
            if request.POST.get(f"delete_{registro.id}") == 'on':
                registro.delete()
        return redirect('overview_dashboard')

    return render(request, 'moneitas/dashboard.html', {
        'current_date': current_date,
        'incomes': incomes,
        'expenses': expenses,
        'balance': balance,
        'selected_month': selected_month,
        'month_choices': month_choices,
        'financial_records': financial_records.order_by('-date'),
        'filter_form': filter_form,
        'dashboard_disabled': True,
    })


