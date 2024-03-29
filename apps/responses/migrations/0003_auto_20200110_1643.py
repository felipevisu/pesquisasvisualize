# Generated by Django 3.0.2 on 2020-01-10 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
        ('responses', '0002_auto_20200110_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='openresponse',
            name='survey',
        ),
        migrations.RemoveField(
            model_name='regionalresponse',
            name='survey',
        ),
        migrations.AddField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='responses', to='surveys.Survey', verbose_name='pesquisa'),
            preserve_default=False,
        ),
    ]
