# Generated by Django 3.1.2 on 2020-10-08 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0015_auto_20201008_1620'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Cidade', 'verbose_name_plural': 'Cidades'},
        ),
        migrations.AlterModelOptions(
            name='neighborhood',
            options={'verbose_name': 'Bairro', 'verbose_name_plural': 'Bairros'},
        ),
        migrations.AlterModelOptions(
            name='sector',
            options={'verbose_name': 'Setor', 'verbose_name_plural': 'Setores'},
        ),
    ]