# Generated by Django 3.1.2 on 2024-07-05 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0033_auto_20201010_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='enumerated',
            field=models.BooleanField(default=False, verbose_name='enumerada'),
        ),
    ]
