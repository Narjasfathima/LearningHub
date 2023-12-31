# Generated by Django 4.2.4 on 2023-09-06 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0071_delete_testmark_remove_test_duration_minutes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField()),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.test')),
            ],
        ),
    ]
