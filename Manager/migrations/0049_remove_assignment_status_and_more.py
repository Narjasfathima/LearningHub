# Generated by Django 4.2.4 on 2023-09-04 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0048_alter_assignment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='status',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]
