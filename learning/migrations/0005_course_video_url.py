# Generated by Django 4.2.4 on 2023-10-28 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0004_course_owner_lesson_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на видео'),
        ),
    ]
