# Generated by Django 4.2.4 on 2023-09-01 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0042_customuser_is_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentmark',
            name='student',
        ),
        migrations.RemoveField(
            model_name='testmark',
            name='student',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
