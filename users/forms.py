from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField()
    lastname = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    name = forms.CharField()
    lastname = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        user: User = kwargs['instance']
        super().__init__(*args, **kwargs)
        self.fields['name'].initial = user.profile.name
        self.fields['lastname'].initial = user.profile.lastname

    def custom_save(self, *args, **kwargs):
        lv: User = self.save(commit=False)
        lv.profile.name = self.cleaned_data['name']
        lv.profile.lastname = self.cleaned_data['lastname']
        lv.save()
        return lv
