# Generated by Django 3.0.2 on 2020-03-23 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20200120_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='logo',
        ),
    ]
