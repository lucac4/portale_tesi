# Generated by Django 4.2.7 on 2023-11-15 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progetti', '0002_alter_progetto_data_creazione_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progetto',
            name='data_creazione',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='progetto',
            name='data_modifica',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
