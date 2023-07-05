# Generated by Django 3.0.2 on 2020-01-20 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0007_auto_20200117_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=200, verbose_name='nome da cidade'),
        ),
        migrations.AlterField(
            model_name='neighborhood',
            name='name',
            field=models.CharField(max_length=200, verbose_name='nome do bairro'),
        ),
        migrations.AlterField(
            model_name='sector',
            name='name',
            field=models.CharField(max_length=200, verbose_name='nome do setor'),
        ),
    ]