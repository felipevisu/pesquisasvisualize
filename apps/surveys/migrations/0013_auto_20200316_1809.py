# Generated by Django 3.0.2 on 2020-03-16 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0010_auto_20200313_2232'),
        ('surveys', '0012_auto_20200127_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regionalsurveyinterviewer',
            name='sectors',
            field=models.ManyToManyField(blank=True, to='locations.Sector', verbose_name='setores'),
        ),
    ]
