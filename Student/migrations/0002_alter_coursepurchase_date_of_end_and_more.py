# Generated by Django 4.2.4 on 2023-09-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursepurchase',
            name='date_of_end',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='coursepurchase',
            name='date_of_join',
            field=models.DateField(null=True),
        ),
    ]