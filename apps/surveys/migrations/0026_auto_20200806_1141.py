# Generated by Django 3.0.4 on 2020-08-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0025_auto_20200806_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='atalho'),
        ),
    ]
