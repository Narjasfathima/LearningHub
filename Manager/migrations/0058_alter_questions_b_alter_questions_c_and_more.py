# Generated by Django 4.2.4 on 2023-09-05 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0057_alter_questions_a_alter_questions_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='B',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='questions',
            name='C',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='questions',
            name='D',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='questions',
            name='answer',
            field=models.CharField(choices=[(models.CharField(max_length=300), 'A'), (models.CharField(max_length=300), 'B'), (models.CharField(max_length=300), 'C'), (models.CharField(max_length=300), 'D')], max_length=100),
        ),
    ]
