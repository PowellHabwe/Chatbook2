# Generated by Django 4.0.5 on 2022-08-22 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_post_video_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(default=1, upload_to='video/%y'),
            preserve_default=False,
        ),
    ]
