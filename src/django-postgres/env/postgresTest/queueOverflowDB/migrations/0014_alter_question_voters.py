# Generated by Django 3.2.8 on 2021-11-12 15:46

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queueOverflowDB', '0013_alter_question_voters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='voters',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=50), null=True, size=None),
        ),
    ]
