# Generated by Django 3.0.4 on 2020-08-06 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0022_auto_20200720_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='opensurvey',
            name='max_responses',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='número de formulários'),
        ),
    ]
