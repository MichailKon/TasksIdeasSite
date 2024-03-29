from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.core.exceptions import PermissionDenied, BadRequest
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, ListView
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ideas.views import IdeaListSerializer
from .models import Contest, Idea, IdeaInContest
from .utilities import check_user_contest_access
from .forms import UpdateContestForm, AddContestForm


class ContestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Contest
    template_name = 'contests/home.html'
    context_object_name = 'contests'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = Paginator(self.object_list, context.get('paginate_by', self.paginate_by))
        context['paginator'] = p
        context['contests'] = p.page(context['page_obj'].number)
        # context['contests'] = IdeaListSerializer(p.page(context['page_obj'].number), many=True).data
        return context

    def get_queryset(self):
        user = self.request.user
        result = Contest.objects
        if not user.is_staff:
            user_groups = user.usergroup_set.all()
            result = result.filter(Q(users_can_view__in=[user.id]) |
                                   Q(users_can_edit__in=[user.id]) |
                                   Q(groups_access__in=user_groups) |
                                   Q(real_author=user))
        return result.distinct().all()

    def test_func(self):
        return self.request.user.is_authenticated


def contest_detail_view(request, pk: int):
    contest = get_object_or_404(Contest, pk=pk)
    user = request.user
    template_name = 'contests/contest_detail.html'
    if not check_user_contest_access(contest, user, check_read=True):
        raise PermissionDenied
    return render(request, template_name, context={"contest": contest,
                                                   "user_can_edit": check_user_contest_access(contest, user,
                                                                                              check_read=False)})


@method_decorator(csrf_exempt, name='dispatch')
class ContestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contest
    form_class = UpdateContestForm
    template_name = 'contests/contest_update.html'

    def get_form_kwargs(self):
        kwargs = super(ContestUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        return check_user_contest_access(self.get_object(), self.request.user, check_read=False)


@method_decorator(csrf_exempt, name='dispatch')
class ContestCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Contest
    form_class = AddContestForm
    template_name = 'contests/contest_create.html'

    def form_valid(self, form):
        form.instance.real_author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated


def contest_delete_view(request, pk: int):
    contest = get_object_or_404(Contest, pk=pk)
    user = request.user
    if not check_user_contest_access(contest, user, False):
        raise PermissionDenied
    contest.delete()
    return redirect('contests-home')


def contest_tasks_update_view(request, pk: int):
    template_name = 'contests/tasks_update.html'
    contest = get_object_or_404(Contest, pk=pk)

    if not check_user_contest_access(contest, request.user, False):
        raise PermissionDenied
    return render(request, template_name, context={"contest": contest})


@method_decorator(csrf_exempt, name='dispatch')
def save_tasks2contest(request, pk: int):
    # maybe have to move it to ajax
    contest = get_object_or_404(Contest, pk=pk)
    if not check_user_contest_access(contest, request.user, False):
        raise PermissionDenied
    problems = request.POST.getlist('problems[]')
    problems_to_add = []
    for i in problems:
        try:
            i = int(i)
        except ValueError:
            raise BadRequest
        prob = get_object_or_404(Idea, pk=i)
        if not check_user_contest_access(contest, request.user, True):
            continue
        problems_to_add.append(prob)
    contest.ideas_list.clear()
    for problem in problems_to_add:
        contest.ideas_list.add(problem)
    return JsonResponse({"status": "success"})
