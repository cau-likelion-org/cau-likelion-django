# Generated by Django 4.1.5 on 2023-03-04 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cumulativeattendance',
            name='attendance',
        ),
    ]
