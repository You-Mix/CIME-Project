# Generated by Django 4.0.4 on 2022-06-07 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soft_cime', '0010_alter_impot_amr_montant_budg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part_impot',
            name='impot',
        ),
        migrations.AddField(
            model_name='impot',
            name='parts_impot',
            field=models.ManyToManyField(to='soft_cime.part_impot'),
        ),
    ]
