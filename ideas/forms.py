from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField, Form
from django_select2.forms import Select2MultipleWidget

from .models import IdeaTag, IdeaType, Idea, IdeaStatus


class FilterForm(Form):
    title_contains = forms.CharField(required=False, label='Название содержит')
    content_contains = forms.CharField(required=False, label='Идея содержит')
    type = ModelChoiceField(widget=Select2MultipleWidget, queryset=IdeaType.objects.all(), required=False, label='Тип')
    tags = ModelChoiceField(widget=Select2MultipleWidget, queryset=IdeaTag.objects.all(), required=False, label='Теги')
    authors = ModelChoiceField(widget=Select2MultipleWidget, queryset=User.objects.all(), required=False,
                               label='Авторы')
    status = ModelChoiceField(widget=Select2MultipleWidget, queryset=IdeaStatus.objects.all(), required=False,
                              label='Статус')

    def __init__(self, *args, **kwargs):
        title_contains = kwargs.pop('title_contains') if 'title_contains' in kwargs else None
        content_contains = kwargs.pop('content_contains') if 'content_contains' in kwargs else None
        idea_type = kwargs.pop('type') if 'type' in kwargs else None
        tags = kwargs.pop('tags') if 'tags' in kwargs else None
        authors = kwargs.pop('authors') if 'authors' in kwargs else None
        status = kwargs.pop('status') if 'status' in kwargs else None
        super().__init__(*args, **kwargs)
        if title_contains:
            self.fields['title_contains'].initial = title_contains
        if content_contains:
            self.fields['content_contains'].initial = content_contains
        if idea_type:
            self.fields['type'].initial = idea_type
        if tags:
            self.fields['tags'].initial = tags
        if authors:
            self.fields['authors'].initial = authors
        if status:
            self.fields['status'].initial = status


class UpdateIdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'content', 'type', 'tags', 'authors', 'users_can_view', 'users_can_edit', 'status')
        widgets = {
            'tags': Select2MultipleWidget,
            'authors': Select2MultipleWidget,
            'users_can_view': Select2MultipleWidget,
            'users_can_edit': Select2MultipleWidget
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].required = False
        self.fields['tags'].required = False
        self.fields['authors'].required = False
        self.fields['users_can_view'].required = False
        self.fields['users_can_edit'].required = False
        self.fields['status'].required = False


class AddIdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'content', 'type', 'tags', 'authors', 'users_can_view', 'users_can_edit', 'status')
        widgets = {
            'tags': Select2MultipleWidget,
            'authors': Select2MultipleWidget,
            'users_can_view': Select2MultipleWidget,
            'users_can_edit': Select2MultipleWidget
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].required = False
        self.fields['tags'].required = False
        self.fields['authors'].required = False
        self.fields['users_can_view'].required = False
        self.fields['users_can_edit'].required = False
        self.fields['status'].required = False
