from .models import Comment


def gather_comments(parent: Comment):
    children = Comment.objects.filter(in_reply_to=parent.pk)
    res = {'comment_data': parent}
    if children:
        res['children'] = [gather_comments(i) for i in children.all()]
    return res
