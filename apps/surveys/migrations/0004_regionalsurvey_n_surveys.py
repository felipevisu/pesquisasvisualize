# Generated by Django 3.0.2 on 2020-01-15 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_auto_20200114_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionalsurvey',
            name='n_surveys',
            field=models.PositiveIntegerField(default=1, verbose_name='número de formulários'),
        ),
    ]