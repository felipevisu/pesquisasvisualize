# Generated by Django 3.0.2 on 2020-01-16 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200116_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='accounts', verbose_name='foto do perfil'),
        ),
    ]
