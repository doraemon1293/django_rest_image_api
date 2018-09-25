# Generated by Django 2.1.1 on 2018-09-24 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='extension',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='transferedimage',
            name='extension',
            field=models.CharField(choices=[('tiff', 'tiff'), ('bmp', 'bmp'), ('jpeg', 'jpeg'), ('webp', 'webp'), ('png', 'png'), ('gif', 'gif')], max_length=100),
        ),
    ]
