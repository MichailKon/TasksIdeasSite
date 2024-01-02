from django.db import models
from ideas.models import Idea, User, UserGroup
from django.urls import reverse


class Contest(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    ideas_list = models.ManyToManyField(Idea, verbose_name='Идеи в контесте', through='IdeaInContest')
    users_can_view = models.ManyToManyField(User, verbose_name='Пользователи, которые могут просматривать',
                                            related_name='contest2person_view')
    users_can_edit = models.ManyToManyField(User, verbose_name='Пользователи, которые могут редактировать',
                                            related_name='contest2person_edit')
    groups_access = models.ManyToManyField(UserGroup, verbose_name='Группы пользователей, которые могут редактировать')
    date_update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    real_author = models.ForeignKey(User, verbose_name='Автор контеста', on_delete=models.SET_NULL, default=None,
                                    null=True)

    def __str__(self):
        return f'Контест {self.name}'

    class Meta:
        ordering = ['-date_update', ]

    def get_absolute_url(self):
        return reverse('contest-detail', kwargs={'pk': self.pk})


class IdeaInContest(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    # task_letter = models.CharField(max_length=10)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

    # class Meta:
    #     ordering = ['-task_letter']
