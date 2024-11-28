# Generated by Django 5.0.9 on 2024-11-22 03:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0002_documento'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformacionAnalizada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.TextField(blank=True, null=True)),
                ('objetivo', models.TextField(blank=True, null=True)),
                ('hipotesis', models.TextField(blank=True, null=True)),
                ('justificacion', models.TextField(blank=True, null=True)),
                ('problema', models.TextField(blank=True, null=True)),
                ('documento', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='proyecto.documento')),
            ],
        ),
    ]