# Generated by Django 4.1.5 on 2023-02-16 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0006_alter_gallery_thumbnail'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Image',
            new_name='GalleryImage',
        ),
    ]
