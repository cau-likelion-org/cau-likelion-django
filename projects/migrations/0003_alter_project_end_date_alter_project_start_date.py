# Generated by Django 4.1.5 on 2023-02-17 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_link_alter_project_team_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.CharField(max_length=20, verbose_name='프로젝트 종료 일자'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.CharField(max_length=20, verbose_name='프로젝트 시작일자'),
        ),
    ]