# Generated by Django 3.0.4 on 2020-07-21 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0019_auto_20200720_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='key',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='chave'),
        ),
    ]
