# Generated by Django 4.1.5 on 2023-03-07 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0014_alter_gallery_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryimage',
            name='image',
            field=models.ImageField(max_length=1000, upload_to='', verbose_name='사진 url'),
        ),
    ]
