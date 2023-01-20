from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Idea, IdeaType, IdeaTag
from .forms import FilterForm


def is_valid_param(param):
    return param is not None and param != '' and param != []


def render_home(request):
    parameters = request.GET
    result = Idea.objects
    if is_valid_param(parameters.get('type')):
        result = result.filter(type=parameters.get('type'))
    if is_valid_param(parameters.getlist('authors')):
        result = result.filter(authors__in=parameters.getlist('authors', [])).distinct()
    if is_valid_param(parameters.getlist('tags')):
        result = result.filter(tags__in=parameters.getlist('tags', [])).distinct()
    if is_valid_param(parameters.get('title_contains')):
        result = result.filter(title__icontains=parameters.get('title_contains'))
    if is_valid_param(parameters.get('content_contains')):
        result = result.filter(content__icontains=parameters.get('content_contains'))
    result = result.order_by("-date_posted")
    return render(request, 'ideas/home.html',
                  {'ideas': result.all(), 'types': IdeaType.objects.all(), 'tags': IdeaTag.objects.all(),
                   'form': FilterForm})


class IdeaDetailView(DetailView):
    model = Idea


class IdeaCreateView(CreateView):
    model = Idea
    fields = ['title', 'content', 'type', 'tags', 'authors']

    def form_valid(self, form):
        return super().form_valid(form)


class IdeaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Idea
    fields = ['title', 'content', 'type', 'tags', 'authors']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        idea = self.get_object()
        if self.request.user in idea.authors.all() or self.request.user.is_staff:
            return True
        return False


class IdeaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Idea
    success_url = '/'

    def test_func(self):
        idea = self.get_object()
        if self.request.user in idea.author.all() or self.request.user.is_staff:
            return True
        return False
