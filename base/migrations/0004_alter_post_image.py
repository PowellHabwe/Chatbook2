# Generated by Django 4.0.5 on 2022-08-22 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_post_video_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(upload_to=''),
        ),
    ]
