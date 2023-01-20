from django.forms import ModelForm, ModelChoiceField, CheckboxSelectMultiple, ChoiceField, SelectMultiple, Form
from django import forms
from .models import Idea, IdeaTag, IdeaType
from django.contrib.auth.models import User


class FilterForm(Form):
    title_contains = forms.CharField(required=False, label='Название содержит')
    content_contains = forms.CharField(required=False, label='Идея содержит')
    type = ModelChoiceField(queryset=IdeaType.objects.all(), required=False, label='Тип')
    tags = ModelChoiceField(widget=SelectMultiple, queryset=IdeaTag.objects.all(), required=False, label='Теги')
    authors = ModelChoiceField(widget=SelectMultiple, queryset=User.objects.all(), required=False, label='Авторы')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
