# Generated by Django 3.0.4 on 2020-07-16 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0017_auto_20200323_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('text', 'text'), ('radio', 'radio'), ('select', 'select'), ('select-multiple', 'select multiple'), ('numeric', 'numeric')], default='radio', max_length=25, verbose_name='tipo de questão'),
        ),
        migrations.AlterField(
            model_name='question',
            name='required',
            field=models.BooleanField(default=True, verbose_name='obrigatório'),
        ),
    ]
