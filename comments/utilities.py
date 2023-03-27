from .models import Comment
from ideas.utilities import check_user_idea_access

from django.contrib.auth.models import User


def gather_comments(parent: Comment):
    children = Comment.objects.filter(in_reply_to=parent.pk)
    res = {'comment_data': parent}
    if children:
        res['children'] = [gather_comments(i) for i in children.all()]
    return res


def check_comment_edit_or_delete_access(comment: Comment, user: User):
    idea = comment.idea
    return check_user_idea_access(idea, user, check_read=False) and (user.is_staff or comment.author == user)
