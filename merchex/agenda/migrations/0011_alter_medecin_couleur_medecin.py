# Generated by Django 5.0.1 on 2024-03-30 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0010_alter_patient_couleur_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medecin',
            name='couleur_medecin',
            field=models.CharField(choices=[('#0000FF', 'Bleu'), ('#FF0000', 'Rouge'), ('#FFFF00', 'Jaune')], default='Bleu', max_length=20),
        ),
    ]