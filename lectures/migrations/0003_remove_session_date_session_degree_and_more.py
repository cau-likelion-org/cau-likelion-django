# Generated by Django 4.1.5 on 2023-02-17 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lectures', '0002_alter_session_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='date',
        ),
        migrations.AddField(
            model_name='session',
            name='degree',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='세션 차수'),
        ),
        migrations.AlterField(
            model_name='session',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자 id값'),
        ),
        migrations.AlterField(
            model_name='sessionimage',
            name='session_id',
            field=models.ForeignKey(db_column='session_id', on_delete=django.db.models.deletion.CASCADE, related_name='image', to='lectures.session', verbose_name='세션id값'),
        ),
    ]