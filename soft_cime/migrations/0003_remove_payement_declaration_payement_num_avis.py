# Generated by Django 4.0.4 on 2022-05-30 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soft_cime', '0002_impot_declare_statut_payement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payement',
            name='declaration',
        ),
        migrations.AddField(
            model_name='payement',
            name='num_avis',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
