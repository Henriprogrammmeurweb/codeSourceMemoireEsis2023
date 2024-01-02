# Generated by Django 4.2.4 on 2023-12-31 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AppPersonnel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Annee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=155, unique=True)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Planning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('annee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppPlanning.annee')),
                ('personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='AppPersonnel.service')),
            ],
        ),
    ]
