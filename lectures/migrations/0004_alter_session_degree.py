# Generated by Django 4.1.5 on 2023-02-17 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0003_remove_session_date_session_degree_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='degree',
            field=models.IntegerField(blank=True, null=True, verbose_name='세션 차수'),
        ),
    ]