from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.views.generic.edit import FormMixin
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .forms import FilterForm, UpdateIdeaForm, AddIdeaForm, AddCommentForm
from .models import Idea, IdeaType, IdeaTag, Comment


def is_valid_param(param):
    if param is None:
        return False
    return any(map(bool, param))


class IdeaListSerializer(ModelSerializer):
    content_shorted = SerializerMethodField()
    tags_list = SerializerMethodField()
    type_name = SerializerMethodField()
    authors_list = SerializerMethodField()
    status_name = SerializerMethodField()
    status_color = SerializerMethodField()
    date_posted = SerializerMethodField()
    date_update = SerializerMethodField()

    class Meta:
        model = Idea
        fields = '__all__'

    @staticmethod
    def get_date_update(obj: Idea):
        return obj.date_update

    @staticmethod
    def get_date_posted(obj: Idea):
        return obj.date_posted

    @staticmethod
    def get_status_color(obj: Idea):
        if not obj.status:
            return ''
        return obj.status.color

    @staticmethod
    def get_status_name(obj: Idea):
        if not obj.status:
            return ''
        return str(obj.status)

    @staticmethod
    def get_authors_list(obj: Idea):
        return ', '.join(str(i) for i in obj.authors.all())

    @staticmethod
    def get_type_name(obj: Idea):
        if not obj.type:
            return ''
        return obj.type.type

    @staticmethod
    def get_tags_list(obj: Idea):
        return ', '.join(i.tag for i in obj.tags.all())

    @staticmethod
    def get_content_shorted(obj: Idea):
        if len(obj.content) < 550:
            return obj.content
        res = ''
        cnt = 0
        add_ellipsis = False
        for num, i in enumerate(obj.content):
            if i == '$':
                cnt ^= 1
            res += i
            if num >= 500 and cnt == 0 or num >= 700:
                add_ellipsis = num + 1 != len(obj.content)
                break
        return res + ('...' if add_ellipsis else '')


class IdeaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Idea
    template_name = 'ideas/home.html'
    context_object_name = 'ideas'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = Paginator(self.object_list, context.get('paginate_by', self.paginate_by))
        context['paginator'] = p
        context['ideas'] = IdeaListSerializer(p.page(context['page_obj'].number), many=True).data
        context |= {'types': IdeaType.objects.all(), 'tags': IdeaTag.objects.all()}
        if 'form_filter' not in context:
            context |= {'form_filter': FilterForm(initial=self.request.GET)}
        return context

    def get_queryset(self):
        user = self.request.user
        parameters = self.request.GET
        print(parameters)
        result = Idea.objects
        if is_valid_param(parameters.get('type')):
            result = result.filter(type=parameters.get('type'))
        if is_valid_param(parameters.getlist('authors')):
            result = result.filter(authors__in=filter(bool, parameters.getlist('authors', [])))
        if is_valid_param(parameters.getlist('tags')):
            result = result.filter(tags__in=filter(bool, parameters.getlist('tags', [])))
        if is_valid_param(parameters.get('title_contains')):
            result = result.filter(title__icontains=parameters.get('title_contains'))
        if is_valid_param(parameters.get('content_contains')):
            result = result.filter(content__icontains=parameters.get('content_contains'))
        if is_valid_param(parameters.get('status')):
            result = result.filter(status=parameters.get('status'))
        if not user.is_staff:
            result = result.filter(Q(users_can_view__in=[user.id]) | Q(real_author=user.id))
        result = result.distinct()
        result = result.order_by("-date_update")
        return result.all()

    def test_func(self):
        return self.request.user.is_authenticated


def handle_leave_comment_view(request):
    user = request.user
    if request.method == 'POST':
        pass
    return redirect('ideas-home')


class IdeaDetailView(FormMixin, LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Idea
    form_class = AddCommentForm
    template_name = 'ideas/idea_detail.html'

    def test_func(self):
        idea = self.get_object()
        user = self.request.user
        if user in idea.users_can_edit.all() or \
                user.is_staff or \
                idea.real_author == user or \
                user in idea.users_can_view.all():
            return True
        return False

    def get_success_url(self):
        self.object: Idea
        return reverse('idea-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.get_form()
        self.object: Idea
        context['comments'] = self.object.comment_set.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        myform = form.save(commit=False)
        myform.author = self.request.user
        myform.idea = self.get_object()
        form.save()
        return super().form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
class IdeaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Idea
    form_class = AddIdeaForm
    template_name = 'ideas/idea_form.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def form_valid(self, form):
        form.instance.real_author = self.request.user
        return super().form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
class IdeaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Idea
    form_class = UpdateIdeaForm
    template_name = 'ideas/idea_update.html'

    def get_form_kwargs(self):
        kwargs = super(IdeaUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        idea = self.get_object()
        user = self.request.user
        if user in idea.users_can_edit.all() or user.is_staff or idea.real_author == user:
            return True
        return False


@method_decorator(csrf_exempt, name='dispatch')
class IdeaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Idea
    success_url = '/'

    def test_func(self):
        idea = self.get_object()
        user = self.request.user
        if user in idea.users_can_edit.all() or user.is_staff or idea.real_author == user:
            return True
        return False
