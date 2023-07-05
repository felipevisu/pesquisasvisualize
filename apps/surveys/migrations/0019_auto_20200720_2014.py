# Generated by Django 3.0.4 on 2020-07-20 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0018_auto_20200716_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='finalized',
            field=models.BooleanField(default=False, verbose_name='finalizado'),
        ),
        migrations.AlterField(
            model_name='question',
            name='chart_type',
            field=models.CharField(choices=[('pie', 'pizza'), ('column', 'coluna'), ('list', 'lista')], default='pie', max_length=25, verbose_name='tipo de gráfico'),
        ),
    ]
