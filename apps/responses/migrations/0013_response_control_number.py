# Generated by Django 3.1.2 on 2024-07-05 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responses', '0012_auto_20201008_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='control_number',
            field=models.CharField(blank=True, help_text='Para idenficar a versão física em pesquisas enumeradas', max_length=10, null=True, verbose_name='Número de controle'),
        ),
    ]