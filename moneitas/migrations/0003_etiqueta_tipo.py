# Generated by Django 4.0.7 on 2023-09-09 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneitas', '0002_registrofinanciero_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='etiqueta',
            name='tipo',
            field=models.CharField(choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto')], default='gasto', max_length=7),
            preserve_default=False,
        ),
    ]
