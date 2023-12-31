# Generated by Django 4.2.4 on 2023-09-04 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0052_rename_note_note_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='total_mark',
            new_name='no_quesions',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='test',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='test',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='test',
            name='status',
        ),
        migrations.RemoveField(
            model_name='testmark',
            name='test',
        ),
        migrations.AddField(
            model_name='questions',
            name='A',
            field=models.CharField(default='option A', max_length=300),
        ),
        migrations.AddField(
            model_name='questions',
            name='B',
            field=models.CharField(default='option A', max_length=300),
        ),
        migrations.AddField(
            model_name='questions',
            name='C',
            field=models.CharField(default='option A', max_length=300),
        ),
        migrations.AddField(
            model_name='questions',
            name='D',
            field=models.CharField(default='option A', max_length=300),
        ),
        migrations.AlterField(
            model_name='questions',
            name='answer',
            field=models.CharField(choices=[(models.CharField(default='option A', max_length=300), 'A'), (models.CharField(default='option A', max_length=300), 'B'), (models.CharField(default='option A', max_length=300), 'C'), (models.CharField(default='option A', max_length=300), 'D')], max_length=100),
        ),
    ]
