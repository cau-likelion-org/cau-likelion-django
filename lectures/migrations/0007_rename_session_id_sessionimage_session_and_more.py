# Generated by Django 4.1.5 on 2023-03-05 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0006_alter_session_track'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sessionimage',
            old_name='session_id',
            new_name='session',
        ),
        migrations.AlterField(
            model_name='session',
            name='thumbnail',
            field=models.CharField(max_length=200, verbose_name='썸네일'),
        ),
        migrations.AlterField(
            model_name='session',
            name='track',
            field=models.IntegerField(blank=True, null=True, verbose_name='트랙'),
        ),
    ]