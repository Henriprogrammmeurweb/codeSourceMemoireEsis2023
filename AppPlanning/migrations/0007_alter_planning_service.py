# Generated by Django 4.2.4 on 2023-10-04 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppPersonnel', '0001_initial'),
        ('AppPlanning', '0006_alter_annee_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planning',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppPersonnel.service'),
        ),
    ]
