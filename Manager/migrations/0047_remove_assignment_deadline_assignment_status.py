# Generated by Django 4.2.4 on 2023-09-04 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0046_alter_course_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='deadline',
        ),
        migrations.AddField(
            model_name='assignment',
            name='status',
            field=models.CharField(default='pending', max_length=100),
        ),
    ]
