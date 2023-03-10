# Generated by Django 4.1.5 on 2023-02-07 17:31

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
            name='Gallery',
            fields=[
                ('gallery_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30, verbose_name='글 제목')),
                ('thumbnail', models.CharField(max_length=30, verbose_name='썸네일')),
                ('description', models.TextField(blank=True, null=True, verbose_name='글 내용')),
                ('month', models.IntegerField(blank=True, null=True, verbose_name='월')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='년도')),
                ('member_id', models.ForeignKey(db_column='member_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자 id값')),
            ],
            options={
                'verbose_name': '갤러리',
                'verbose_name_plural': '갤러리',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image_url', models.CharField(max_length=100, verbose_name='사진 url')),
                ('gallery_id', models.ForeignKey(db_column='gallery_id', on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='galleries.gallery', verbose_name='갤러리id값')),
            ],
            options={
                'verbose_name': '사진',
                'verbose_name_plural': '사진들',
            },
        ),
    ]
