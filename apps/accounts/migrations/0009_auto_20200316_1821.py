# Generated by Django 3.0.2 on 2020-03-16 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200120_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='primeiro nome'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='sobrenome'),
        ),
    ]
