from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    lastname = models.CharField(max_length=100, blank=False)
    telegram_login = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.lastname} ({self.user.username})'

    def save(self, **kwargs):
        super().save(**kwargs)


class UserGroup(models.Model):
    name = models.CharField(max_length=200, blank=False)
    users = models.ManyToManyField(User, verbose_name='Пользователи в группе')

    def __str__(self):
        return f'{self.name} (Группа пользователей)'


def user_str(self: User):
    return f'{self.profile.name} {self.profile.lastname} ({self.username})'


if __name__ == '__main__':
    User.add_to_class("__str__", user_str)
