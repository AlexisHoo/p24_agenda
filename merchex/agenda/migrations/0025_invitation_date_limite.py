# Generated by Django 5.0.1 on 2024-05-02 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0024_remove_invitation_date_limite_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='date_limite',
            field=models.DateField(blank=True, null=True),
        ),
    ]
