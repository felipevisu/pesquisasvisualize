# Generated by Django 3.0.2 on 2020-01-17 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_regionalsurveyinterviewer_surveyinterviewer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='regionalsurvey',
            old_name='n_surveys',
            new_name='max_responses',
        ),
    ]
