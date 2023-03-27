from copy import deepcopy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, ListView
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from comments.forms import AddCommentForm, UpdateCommentForm
from comments.utilities import gather_comments
from .forms import FilterForm, UpdateIdeaForm, AddIdeaForm
from .models import Idea, IdeaType, IdeaTag
from .utilities import check_user_idea_access


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
            init = deepcopy(self.request.GET)
            init['authors'] = init.getlist('authors', [])
            init['tags'] = init.getlist('tags', [])

            context |= {'form_filter': FilterForm(initial=init)}
        return context

    def get_queryset(self):
        user = self.request.user
        parameters = self.request.GET
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
            user_groups = user.usergroup_set.all()
            result = result.filter(Q(users_can_view__in=[user.id]) |
                                   Q(real_author=user.id) |
                                   Q(users_can_edit__in=[user.id]) |
                                   Q(groups_access__in=user_groups))
        result = result.distinct()
        result = result.order_by("-date_update")
        return result.all()

    def test_func(self):
        return self.request.user.is_authenticated


def idea_detail_view(request, pk: int):
    idea = get_object_or_404(Idea, pk=pk)
    user = request.user
    template_name = 'ideas/idea_detail.html'
    if not check_user_idea_access(idea, user, check_read=True):
        raise PermissionDenied
    parent_comments = idea.comment_set.filter(in_reply_to=None)
    comments = [gather_comments(parent) for parent in parent_comments]
    return render(request, template_name, {'idea': idea,
                                           'comments': comments,
                                           'user_can_edit': check_user_idea_access(idea, user, check_read=False),
                                           'add_comment_form': AddCommentForm(),
                                           'update_comment_form': UpdateCommentForm()})


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
        return check_user_idea_access(self.get_object(), self.request.user, check_read=False)


def idea_delete_view(request, pk: int):
    idea = get_object_or_404(Idea, pk=pk)
    user = request.user
    if not check_user_idea_access(idea, user):
        raise PermissionDenied
    idea.delete()
    return redirect('ideas-home')
