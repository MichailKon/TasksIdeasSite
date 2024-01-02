from django.http import JsonResponse

from ideas.models import Idea
from collections import defaultdict
from contests.utilities import check_user_contest_access
from ideas.utilities import check_user_idea_access
from ideas.views import IdeaListSerializer


def get_ideas_by_query(request):
    data = Idea.objects.select_related('real_author').all()
    res = defaultdict(list)
    for i in data:
        if not check_user_idea_access(i, request.user, True):
            continue  # Maybe I have to do it a bit more effective
        res["ideas"].append({
            "pk": str(i.pk),
            "title": i.title,
            "short_content": IdeaListSerializer.get_content_shorted100(i),
            "modif": i.date_update,
            "tags": ', '.join(map(lambda x: x[0], i.tags.all().values_list('tag'))),
            "contests": [{'pk': j.pk, 'name': j.name} for j in i.contest_set.all() if
                         check_user_contest_access(j, request.user, True)]
        })
    return JsonResponse(res)
