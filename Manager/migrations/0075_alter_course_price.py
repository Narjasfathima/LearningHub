# Generated by Django 4.2.4 on 2023-09-12 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0074_student_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]
