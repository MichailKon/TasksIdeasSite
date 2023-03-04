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


class IdeaStatus(models.Model):
    status = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.status


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
    status = models.ForeignKey(IdeaStatus, on_delete=models.SET_DEFAULT, default=None, null=True, verbose_name='Статус')
    short_editorial = models.TextField(verbose_name='Идея решения', default='')

    class Meta:
        ordering = ['-date_update', ]

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('idea-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст', null=False)
    date_posted = models.DateTimeField(verbose_name='Дата комментария', auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)  # Maybe I need verbose name, but IDK what to write here :(

    class Meta:
        ordering = ['date_posted', ]


def user_str(self: User):
    return f'{self.profile.name} {self.profile.lastname} ({self.username})'


User.add_to_class("__str__", user_str)
