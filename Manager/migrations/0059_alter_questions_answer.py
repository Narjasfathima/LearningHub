# Generated by Django 4.2.4 on 2023-09-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0058_alter_questions_b_alter_questions_c_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='answer',
            field=models.CharField(choices=[(models.CharField(max_length=300), 'option A'), (models.CharField(max_length=300), 'B'), (models.CharField(max_length=300), 'C'), (models.CharField(max_length=300), 'D')], max_length=300),
        ),
    ]
