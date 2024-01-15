# Generated by Django 3.0.8 on 2023-12-21 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='hora_final',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='hora_inicio',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
