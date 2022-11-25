from django.urls import reverse_lazy
from unidecode import unidecode

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser

from .slug import unique_slugify


class MyUser(AbstractUser):
    profile_picture = models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d', verbose_name='Фотография профиля')


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(blank=True, null=True, verbose_name='Содержание')
    tags = models.ManyToManyField('Tag', verbose_name='Теги', related_name='questions_by_tag', blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, blank=True, null=True)
    likes = models.ManyToManyField(get_user_model(), verbose_name='Лайки', related_name='questions_liked_by_user', blank=True)
    dislikes = models.ManyToManyField(get_user_model(), verbose_name='Дизлайки', related_name='question_disliked_by_user', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')  # Переделать механизм

    def save(self, **kwargs):
        slug = unidecode(str(self.title))
        unique_slugify(self, slug)
        super().save(**kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('question_detail', args=[self.slug])


class Comment(models.Model):
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, blank=True, null=True)
    is_solution = models.BooleanField(default=False, verbose_name='Решение вопроса')
    likes = models.ManyToManyField(get_user_model(), verbose_name='Лайки', related_name='comments_liked_by_user', blank=True)
    dislikes = models.ManyToManyField(get_user_model(), verbose_name='Дизлайки', related_name='comments_disliked_by_user', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')  # Переделать механизм

    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тэг')
    slug = models.SlugField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('questions_by_tag', args=[self.slug])
