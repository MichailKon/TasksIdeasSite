from django.contrib.auth.models import User
from .models import Idea


def check_user_idea_access(idea: Idea, user: User, check_read: bool):
    if user.is_staff or \
            idea.real_author == user or \
            user in idea.users_can_edit.all() or \
            any(user in rel.users.all() for rel in idea.groups_access.all()):
        return True
    if idea.contest_set.filter(real_author=user.id) or \
            idea.contest_set.filter(users_can_edit__in=[user.id]) or \
            idea.contest_set.filter(groups_access__in=user.usergroup_set.all()):
        return True
    if check_read and user in idea.users_can_view.all():
        return True
    if check_read and idea.contest_set.filter(users_can_view__in=[user.id]):
        return True
    return False


def is_valid_param(param):
    if param is None:
        return False
    return any(map(bool, param))
