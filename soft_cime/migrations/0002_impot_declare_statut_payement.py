# Generated by Django 4.0.4 on 2022-05-30 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soft_cime', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='impot_declare',
            name='statut_payement',
            field=models.BooleanField(default=0),
        ),
    ]
