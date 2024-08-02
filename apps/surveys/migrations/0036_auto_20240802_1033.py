# Generated by Django 3.1.2 on 2024-08-02 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0035_auto_20240704_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='enumerated',
            field=models.BooleanField(default=False, help_text='Para pesquisas feitas no papel enumerado o número de série de cada questionário deverá ser informado', verbose_name='enumerada'),
        ),
    ]
