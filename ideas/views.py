from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Idea


def home(request):
    context = {
        'ideas': Idea.objects.all()
    }
    return render(request, 'ideas/home.html', context)


class IdeaListView(ListView):
    model = Idea
    template_name = 'ideas/home.html'
    context_object_name = 'ideas'
    ordering = ['-date_posted', ]


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
        if self.request.user in idea.author.all():
            return True
        return False
