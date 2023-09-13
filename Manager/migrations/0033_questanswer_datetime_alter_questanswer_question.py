# Generated by Django 4.2.4 on 2023-08-31 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0032_questanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='questanswer',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='questanswer',
            name='question',
            field=models.CharField(max_length=500, verbose_name=''),
        ),
    ]
