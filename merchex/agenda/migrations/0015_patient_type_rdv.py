# Generated by Django 5.0.1 on 2024-04-28 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0014_alter_type_rdv_duree'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='type_rdv',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='agenda.type_rdv'),
        ),
    ]