# Generated by Django 4.1.3 on 2022-11-22 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0012_tag_question_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Тэг'),
        ),
    ]
