"""moneitas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('create_record/', views.create_financial_record, name='create_record'),
    path('create_record/<int:edit>/', views.create_financial_record, name='create_record'),
    path('get_labels/', views.get_labels, name='get_labels'),
    path('labels/', views.list_labels, name='list_labels'),
    path('create_label/', views.create_label, name='create_label'),
    path('create_label/<int:edit>/', views.create_label, name='create_label'),
    path('', views.overview_dashboard, name='overview_dashboard'),
    path('navbar/', TemplateView.as_view(template_name='moneitas/navbar.html'), name='navbar'),
    path('todo/', views.todo, name='todo'),
    path('api/create_task/', views.create_task, name='create_task'),
    path('api/delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('api/edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
]
