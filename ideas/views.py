from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .forms import FilterForm, UpdateIdeaForm, AddIdeaForm
from .models import Idea, IdeaType, IdeaTag


def is_valid_param(param):
    if param is None or param in ['', []]:
        return False
    return any(map(lambda x: x, param))


def render_home(request):
    parameters = request.GET
    result = Idea.objects
    filter_form_params = {}
    if is_valid_param(parameters.get('type')):
        result = result.filter(type=parameters.get('type'))
        filter_form_params['type'] = parameters.get('type')
    if is_valid_param(parameters.getlist('authors')):
        result = result.filter(authors__in=filter(lambda x: x, parameters.getlist('authors', []))).distinct()
        filter_form_params['authors'] = list(filter(lambda x: x, parameters.getlist('authors', [])))
    if is_valid_param(parameters.getlist('tags')):
        result = result.filter(tags__in=filter(lambda x: x, parameters.getlist('tags', []))).distinct()
        filter_form_params['tags'] = list(filter(lambda x: x, parameters.getlist('tags', [])))
    if is_valid_param(parameters.get('title_contains')):
        result = result.filter(title__icontains=parameters.get('title_contains'))
        filter_form_params['title_contains'] = parameters.get('title_contains')
    if is_valid_param(parameters.get('content_contains')):
        result = result.filter(content__icontains=parameters.get('content_contains'))
        filter_form_params['content_contains'] = parameters.get('content_contains')
    if not request.user.is_authenticated:
        result = Idea.objects.none()
    elif not request.user.is_staff:
        result = result.filter(Q(users_can_view__in=[request.user.id]) | Q(real_author=request.user.id))
    result = result.order_by("-date_update")
    form = FilterForm(**filter_form_params)
    return render(request, 'ideas/home.html',
                  {'ideas': result.all(), 'types': IdeaType.objects.all(), 'tags': IdeaTag.objects.all(),
                   'form_filter': form})


class IdeaDetailView(DetailView):
    model = Idea


class IdeaCreateView(CreateView):
    model = Idea
    form_class = AddIdeaForm
    template_name = 'ideas/idea_form.html'

    def form_valid(self, form):
        form.instance.real_author = self.request.user
        return super().form_valid(form)


class IdeaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Idea
    form_class = UpdateIdeaForm
    template_name = 'ideas/idea_update.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        idea = self.get_object()
        user = self.request.user
        if user in idea.users_can_edit.all() or user.is_staff or idea.real_author == user:
            return True
        return False


class IdeaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Idea
    success_url = '/'

    def test_func(self):
        idea = self.get_object()
        user = self.request.user
        if user in idea.users_can_edit.all() or user.is_staff or idea.real_author == user:
            return True
        return False
