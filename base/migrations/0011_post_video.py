# Generated by Django 4.0.5 on 2022-08-22 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_remove_post_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(default=1, upload_to='video/%y'),
            preserve_default=False,
        ),
    ]
