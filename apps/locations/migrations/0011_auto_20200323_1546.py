# Generated by Django 3.0.2 on 2020-03-23 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0010_auto_20200313_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neighborhood',
            name='max_responses',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='total de questionários'),
        ),
    ]