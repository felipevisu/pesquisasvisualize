# Generated by Django 3.0.4 on 2020-08-06 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0024_opensurvey_open_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='atalho'),
        ),
        migrations.AlterField(
            model_name='opensurvey',
            name='open_form',
            field=models.BooleanField(default=False, verbose_name='formulário aberto ao público'),
        ),
    ]
