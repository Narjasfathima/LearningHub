# Generated by Django 4.2.4 on 2023-09-01 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0036_alter_student_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
