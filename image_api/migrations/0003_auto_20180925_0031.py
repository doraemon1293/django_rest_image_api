# Generated by Django 2.1.1 on 2018-09-24 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_api', '0002_auto_20180925_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferedimage',
            name='extension',
            field=models.CharField(max_length=100),
        ),
    ]
