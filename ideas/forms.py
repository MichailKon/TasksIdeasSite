from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField, Form, HiddenInput
from django_select2.forms import Select2MultipleWidget

from .models import IdeaTag, IdeaType, Idea, IdeaStatus, Difficulty


class FilterForm(Form):
    title_contains = forms.CharField(required=False, label='Название содержит')
    content_contains = forms.CharField(required=False, label='Идея содержит')
    type = ModelChoiceField(queryset=IdeaType.objects.all(), required=False, label='Тип')
    difficulty = ModelChoiceField(widget=Select2MultipleWidget, queryset=Difficulty.objects.all(), required=False,
                                  label='Сложность')
    tags = ModelChoiceField(widget=Select2MultipleWidget, queryset=IdeaTag.objects.all(), required=False, label='Теги')
    authors = ModelChoiceField(widget=Select2MultipleWidget, queryset=User.objects.all(), required=False,
                               label='Авторы')
    status = ModelChoiceField(queryset=IdeaStatus.objects.all(), required=False,
                              label='Статус')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UpdateIdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = (
            'title', 'content', 'short_editorial', 'type', 'difficulty', 'tags', 'authors', 'users_can_view',
            'users_can_edit', 'groups_access', 'status', 'polygon_task')
        widgets = {
            'tags': Select2MultipleWidget,
            'authors': Select2MultipleWidget,
            'users_can_view': Select2MultipleWidget,
            'users_can_edit': Select2MultipleWidget,
            'groups_access': Select2MultipleWidget,
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['type'].required = False
        self.fields['tags'].required = False
        self.fields['authors'].required = False
        self.fields['users_can_view'].required = False
        self.fields['users_can_edit'].required = False
        self.fields['groups_access'].required = False
        self.fields['short_editorial'].required = False
        self.fields['status'].required = False
        self.fields['difficulty'].required = False
        self.fields['polygon_task'].required = False
        if request is None or (request.user is None or not request.user.is_staff):
            self.fields['status'].widget = HiddenInput()


class AddIdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = (
            'title', 'content', 'short_editorial', 'type', 'difficulty', 'tags', 'authors', 'users_can_view',
            'users_can_edit', 'groups_access', 'polygon_task')
        widgets = {
            'tags': Select2MultipleWidget,
            'authors': Select2MultipleWidget,
            'users_can_view': Select2MultipleWidget,
            'users_can_edit': Select2MultipleWidget,
            'groups_access': Select2MultipleWidget
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].required = False
        self.fields['tags'].required = False
        self.fields['authors'].required = False
        self.fields['users_can_view'].required = False
        self.fields['users_can_edit'].required = False
        self.fields['groups_access'].required = False
        self.fields['short_editorial'].required = False
        self.fields['difficulty'].required = False
        self.fields['polygon_task'].required = False
