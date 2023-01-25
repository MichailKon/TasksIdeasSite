from django.contrib.auth.models import User
from django.db import models
from django.contrib import auth


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    lastname = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.name} {self.lastname} ({self.user.username})'

    def save(self, **kwargs):
        super().save(**kwargs)


def user_str(self: User):
    return f'{self.profile.name} {self.profile.lastname} ({self.username})'


if __name__ == '__main__':
    User.add_to_class("__str__", user_str)
