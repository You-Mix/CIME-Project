# Generated by Django 4.0.4 on 2022-06-10 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soft_cime', '0011_remove_part_impot_impot_impot_parts_impot'),
    ]

    operations = [
        migrations.AddField(
            model_name='ug',
            name='activite',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
