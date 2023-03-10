# Generated by Django 4.1.5 on 2023-02-17 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0008_alter_galleryimage_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='month',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='year',
        ),
        migrations.AddField(
            model_name='gallery',
            name='date',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='gallery_id',
            field=models.ForeignKey(db_column='gallery_id', on_delete=django.db.models.deletion.CASCADE, related_name='image', to='galleries.gallery', verbose_name='갤러리id값'),
        ),
    ]
