def check_user_idea_access(idea, user, check_read=True):
    if user.is_staff or \
            idea.real_author == user or \
            user in idea.users_can_edit.all() or \
            any(user in rel.users.all() for rel in idea.groups_access.all()):
        return True
    if check_read and user in idea.users_can_view.all():
        return True
    return False
