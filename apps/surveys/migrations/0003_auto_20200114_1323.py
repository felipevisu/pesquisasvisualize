# Generated by Django 3.0.2 on 2020-01-14 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_auto_20200110_1703'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['order'], 'verbose_name': 'Pergunta', 'verbose_name_plural': 'Perguntas'},
        ),
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='ordem'),
        ),
    ]
