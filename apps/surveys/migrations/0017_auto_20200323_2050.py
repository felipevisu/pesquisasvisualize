# Generated by Django 3.0.2 on 2020-03-23 23:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0016_auto_20200323_2049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='regionalsurvey',
            old_name='max_responses_s',
            new_name='max_responses',
        ),
    ]