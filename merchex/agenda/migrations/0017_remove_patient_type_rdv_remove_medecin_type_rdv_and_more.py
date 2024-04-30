# Generated by Django 5.0.1 on 2024-04-29 23:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0016_medecin_type_rdv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='type_rdv',
        ),
        migrations.RemoveField(
            model_name='medecin',
            name='type_rdv',
        ),
        migrations.CreateModel(
            name='TypeRDV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duree', models.DurationField(default='00:45:00')),
                ('tel_medecin', models.CharField(help_text='Type de RDV', max_length=25)),
                ('medecins', models.ManyToManyField(to='agenda.medecin')),
            ],
        ),
        migrations.CreateModel(
            name='RDVPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.patient')),
                ('type_rdv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.typerdv')),
            ],
        ),
        migrations.DeleteModel(
            name='type_RDV',
        ),
    ]