# Generated by Django 5.0.1 on 2024-03-30 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0009_alter_medecin_profession_alter_medecin_tel_medecin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='couleur_patient',
            field=models.CharField(choices=[('#0000FF', 'Bleu'), ('#FF0000', 'Rouge'), ('#FFFF00', 'Jaune')], default='Bleu', max_length=20),
        ),
    ]
