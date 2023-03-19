from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from comments.models import Comment
from ideas.views import check_user_idea_access
from ideas.models import Idea


def get_idea(request, idea_pk: int):
    user = request.user
    idea = get_object_or_404(Idea, pk=idea_pk)
    if not check_user_idea_access(idea, user, check_read=True):
        raise PermissionDenied
    users_with_access = set(idea.users_can_view.values_list('pk', flat=True)) | set(
        idea.users_can_edit.values_list('pk', flat=True)) | {idea.real_author.pk}
    for i in idea.groups_access.all():
        users_with_access |= set(i.users.values_list('pk', flat=True))

    return JsonResponse({'comments': list(idea.comment_set.values_list('pk', flat=True)),
                         'title': idea.title,
                         'authors': list(idea.authors.values_list('pk', flat=True)),
                         'users_with_access': list(users_with_access)})


def get_user_info(request, user_pk: int):
    user = request.user
    if not user.is_authenticated:
        raise PermissionDenied
    user = get_object_or_404(User, pk=user_pk)
    return JsonResponse({'username': user.username,
                         'name': user.profile.name,
                         'lastname': user.profile.lastname,
                         'telegram_login': user.profile.telegram_login})


def get_ideas_with_access(request):
    user = request.user
    if not user.is_authenticated:
        raise PermissionDenied
    ideas = list(Idea.objects.filter(Q(real_author=user) |
                                     Q(users_can_edit__in=[user]) |
                                     Q(users_can_view__in=[user]) |
                                     Q(groups_access__users__in=[user])).values_list('pk',
                                                                                     flat=True))
    return JsonResponse({'ideas': ideas})


def get_comment(request, comment_pk: int):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_pk)
    if not check_user_idea_access(comment.idea, user, check_read=True):
        raise PermissionDenied
    return JsonResponse({'text': comment.text,
                         'author': comment.author.pk})
