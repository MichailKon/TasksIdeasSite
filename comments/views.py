from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect

from ideas.models import Idea
from ideas.utilities import check_user_idea_access
from .forms import AddCommentForm, UpdateCommentForm
from .models import Comment
from .utilities import check_comment_edit_or_delete_access


def delete_comment_by_user_request(request, pk: int):
    user = request.user
    comment = get_object_or_404(Comment, pk=pk)
    if not check_comment_edit_or_delete_access(comment, user):
        raise PermissionDenied
    idea = comment.idea
    comment.delete()
    return redirect('idea-detail', idea.pk)


def update_comment_by_user_request(request, pk: int):
    user = request.user
    comment = get_object_or_404(Comment, pk=pk)
    idea = comment.idea
    if not check_comment_edit_or_delete_access(comment, user):
        raise PermissionDenied
    if comment.author != user:
        raise PermissionDenied
    if request.method != 'POST':
        return redirect('idea-detail', idea.pk)
    form = UpdateCommentForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['text']
        comment.text = text
        comment.save()
    return redirect('idea-detail', idea.pk)


def create_comment_by_user_request(request, pk: int, in_reply: int = -1):
    user = request.user
    idea = get_object_or_404(Idea, pk=pk)
    if in_reply != -1:
        in_reply_to = get_object_or_404(Comment, pk=in_reply)
    if not check_user_idea_access(idea, user, check_read=False):
        raise PermissionDenied
    if request.method != 'POST':
        return redirect('idea-detail', idea.pk)
    form = AddCommentForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['text']
        if in_reply > -1:
            Comment(text=text, author=user, idea=idea, in_reply_to=in_reply_to).save()
        else:
            Comment(text=text, author=user, idea=idea).save()
    return redirect('idea-detail', idea.pk)
