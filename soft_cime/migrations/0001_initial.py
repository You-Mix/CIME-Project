# Generated by Django 4.0.4 on 2022-05-30 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cellule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='contribuable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NIU', models.CharField(max_length=200)),
                ('raison_social', models.CharField(max_length=200)),
                ('activite', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=200, verbose_name='Téléphone')),
                ('arrondissement', models.CharField(max_length=200)),
                ('statut', models.CharField(choices=[('actif', 'Actif'), ('inactif', 'Inactif')], default='Actif', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Declaration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_avis', models.PositiveIntegerField()),
                ('chiffre_affaire', models.PositiveBigIntegerField()),
                ('date_limite', models.DateField()),
                ('date_emission', models.DateTimeField(auto_now=True)),
                ('contribuable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.contribuable')),
            ],
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departement', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Impot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impot', models.CharField(max_length=30, verbose_name='Impôt')),
                ('type_impot', models.CharField(choices=[('Budgétaire', 'Budgétaire'), ('Totalement Bugétaire', 'Totalement Bugétaire'), ('Non Budgétaire', 'Non Budgétaire')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Regime_impot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regime_impot', models.CharField(choices=[('RPM', 'RPM'), ('RPP', 'RPP'), ('HRI', "Hors régime d'imposition")], max_length=20, verbose_name="Régime d'imposition")),
            ],
        ),
        migrations.CreateModel(
            name='UG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ug', models.PositiveIntegerField(verbose_name='Unité de gestion')),
            ],
        ),
        migrations.CreateModel(
            name='Sous_secteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=200, verbose_name='Libéllé du sous unité de gestion')),
                ('ug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.ug')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('cellule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.cellule')),
            ],
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=20, unique=True)),
                ('nom', models.CharField(max_length=200)),
                ('poste', models.CharField(max_length=200)),
                ('cellule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.cellule')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='soft_cime.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('montant', models.PositiveIntegerField()),
                ('contribuable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.contribuable')),
                ('declaration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='soft_cime.declaration')),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.personnel')),
            ],
        ),
        migrations.CreateModel(
            name='Impot_Declare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.PositiveIntegerField()),
                ('declaration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.declaration')),
                ('impot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.impot')),
            ],
        ),
        migrations.AddField(
            model_name='declaration',
            name='impots',
            field=models.ManyToManyField(through='soft_cime.Impot_Declare', to='soft_cime.impot'),
        ),
        migrations.AddField(
            model_name='declaration',
            name='personnel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.personnel'),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='departement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.departement'),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='impots',
            field=models.ManyToManyField(to='soft_cime.impot'),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='regime_impot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='soft_cime.regime_impot'),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='sous_secteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.sous_secteur'),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='ug',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soft_cime.ug', verbose_name='Unité de gestion'),
        ),
    ]
