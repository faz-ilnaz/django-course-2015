from django import forms
from django.contrib.auth.models import User
from django import template
from django.forms import RadioSelect

from main_app.models import Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(widget=RadioSelect, choices=Profile.GENDER)
    about_me = forms.Textarea()
    birth_date = forms.DateField(widget=forms.DateInput(format = '%d.%m.%Y'),
                                 input_formats=('%d.%m.%Y',), required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('gender', 'birth_date', 'about_me', 'avatar')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')