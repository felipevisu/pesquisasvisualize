# Generated by Django 3.1.2 on 2020-10-06 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0030_question_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regionalsurvey',
            name='meta',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
