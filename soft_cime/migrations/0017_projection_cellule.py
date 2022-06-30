# Generated by Django 4.0.4 on 2022-06-24 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soft_cime', '0016_projection_impot'),
    ]

    operations = [
        migrations.AddField(
            model_name='projection',
            name='cellule',
            field=models.CharField(choices=[('GESTION ET SUIVI', 'Gestion et suivi'), ('RECOUVREMENT', 'Recouvrement'), ('CONTROLE', 'Controle')], max_length=30, null=True),
        ),
    ]
