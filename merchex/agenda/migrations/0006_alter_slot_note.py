# Generated by Django 5.0.1 on 2024-02-26 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_slot_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='note',
            field=models.CharField(default='Aucunes notes', max_length=400),
        ),
    ]
