# Generated by Django 4.2.4 on 2023-09-05 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0062_test_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='is_question',
            field=models.BooleanField(default=False),
        ),
    ]
