from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField, Form, HiddenInput
from django_select2.forms import Select2MultipleWidget

from .models import Contest, IdeaInContest


class UpdateContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ('name', 'ideas_list', 'users_can_view', 'users_can_edit', 'groups_access')

        widgets = {
            'users_can_view': Select2MultipleWidget,
            'users_can_edit': Select2MultipleWidget,
            'groups_access': Select2MultipleWidget,
            'ideas_list': Select2MultipleWidget
        }

    def __init__(self, *args, **kwargs):
        requests = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['users_can_view'].required = False
        self.fields['users_can_edit'].required = False
        self.fields['groups_access'].required = False
        self.fields['ideas_list'].required = False


class AddContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ('name', 'ideas_list', 'users_can_view', 'users_can_edit', 'groups_access')

        widgets = {
            'users_can_view': Select2MultipleWidget,
            'users_can_edit': Select2MultipleWidget,
            'groups_access': Select2MultipleWidget,
            'ideas_list': Select2MultipleWidget
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users_can_view'].required = False
        self.fields['users_can_edit'].required = False
        self.fields['groups_access'].required = False
        self.fields['ideas_list'].required = False
