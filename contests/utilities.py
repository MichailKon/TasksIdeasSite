def check_user_contest_access(contest, user, check_read=True):  # well, duplicated code for now...
    if user.is_staff or \
            contest.real_author == user or \
            user in contest.users_can_edit.all() or \
            any(user in rel.users.all() for rel in contest.groups_access.all()):
        return True
    if check_read and user in contest.users_can_view.all():
        return True
    return False
