# Generated by Django 4.1.5 on 2023-03-04 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0005_session_date_session_reference_alter_session_track'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='track',
            field=models.CharField(choices=[('front', 'front'), ('back', 'back'), ('design', 'design'), ('pm', 'pm')], max_length=10, verbose_name='트랙'),
        ),
    ]