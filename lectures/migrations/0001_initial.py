# Generated by Django 4.1.5 on 2023-02-16 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('track', models.IntegerField(verbose_name='트랙')),
                ('thumbnail', models.ImageField(max_length=200, upload_to='', verbose_name='썸네일')),
                ('description', models.TextField(blank=True, null=True, verbose_name='글 내용')),
                ('presenter', models.CharField(max_length=10, verbose_name='발표자')),
                ('topic', models.CharField(max_length=50, verbose_name='세션 주제')),
                ('date', models.DateField(verbose_name='세션날짜')),
                ('user_id', models.ForeignKey(db_column='member_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자 id값')),
            ],
            options={
                'verbose_name': '세션',
                'verbose_name_plural': '세션',
            },
        ),
        migrations.CreateModel(
            name='SessionImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='', verbose_name='사진 url')),
                ('session_id', models.ForeignKey(db_column='session_id', on_delete=django.db.models.deletion.CASCADE, related_name='Sessionimage', to='lectures.session', verbose_name='세션id값')),
            ],
            options={
                'verbose_name': '세션사진',
                'verbose_name_plural': '세션사진들',
            },
        ),
    ]
