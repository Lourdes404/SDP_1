# Generated by Django 5.0.9 on 2024-11-22 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0003_informacionanalizada'),
    ]

    operations = [
        migrations.AddField(
            model_name='informacionanalizada',
            name='nombre',
            field=models.TextField(blank=True, null=True),
        ),
    ]
