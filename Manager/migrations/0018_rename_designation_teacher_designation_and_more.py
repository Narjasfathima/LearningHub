# Generated by Django 4.2.4 on 2023-08-29 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0017_alter_teacher_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='Designation',
            new_name='designation',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='Qualification',
            new_name='qualification',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='User',
            new_name='user',
        ),
    ]
