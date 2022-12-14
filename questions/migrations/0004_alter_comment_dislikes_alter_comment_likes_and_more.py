# Generated by Django 4.1.3 on 2022-11-18 07:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_comment_author_question_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL, verbose_name='Дизлайки'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL, verbose_name='Лайки'),
        ),
        migrations.AlterField(
            model_name='question',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='question_dislikes', to=settings.AUTH_USER_MODEL, verbose_name='Дизлайки'),
        ),
        migrations.AlterField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='question_likes', to=settings.AUTH_USER_MODEL, verbose_name='Лайки'),
        ),
    ]
