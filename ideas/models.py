from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class IdeaType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class IdeaTag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class Idea(models.Model):
    title = models.TextField(verbose_name='Название')
    content = models.TextField(verbose_name='Идея')
    real_author = models.ForeignKey(User, verbose_name='Автор записи', on_delete=models.CASCADE)
    type = models.ForeignKey(IdeaType, on_delete=models.SET_DEFAULT, verbose_name='Тип', default=None, null=True)
    tags = models.ManyToManyField(IdeaTag, verbose_name='Теги')
    date_update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    date_posted = models.DateTimeField(verbose_name='Дата записи', default=timezone.now)
    authors = models.ManyToManyField(User, verbose_name='Авторы', related_name='idea2authors')
    users_can_view = models.ManyToManyField(User, verbose_name='Пользователи, которые могут просматривать',
                                            related_name='idea2person_view')
    users_can_edit = models.ManyToManyField(User, verbose_name='Пользователи, которые могут редактировать',
                                            related_name='idea2person_edit')

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('idea-detail', kwargs={'pk': self.pk})


def user_str(self: User):
    return f'{self.profile.name} {self.profile.lastname} ({self.username})'


User.add_to_class("__str__", user_str)
