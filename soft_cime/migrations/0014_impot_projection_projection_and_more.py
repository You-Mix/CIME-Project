# Generated by Django 4.0.4 on 2022-06-21 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soft_cime', '0013_impot_impot_nom_payement_date_virement_payement_etat_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Impot_Projection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('montant', models.PositiveIntegerField()),
                ('impot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.impot')),
            ],
        ),
        migrations.CreateModel(
            name='Projection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('contribuable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.contribuable')),
                ('impots', models.ManyToManyField(through='soft_cime.Impot_Projection', to='soft_cime.impot')),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.personnel')),
            ],
        ),
        migrations.AddField(
            model_name='impot_projection',
            name='projection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.projection'),
        ),
    ]
