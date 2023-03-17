from django.contrib.auth.models import User
from django.db import models

from ideas.models import Idea


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст', null=False)
    date_posted = models.DateTimeField(verbose_name='Дата комментария', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)  # Maybe I need verbose name, but IDK what to write here :(
    in_reply_to = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} {self.text}'

    class Meta:
        ordering = ['date_posted', ]
