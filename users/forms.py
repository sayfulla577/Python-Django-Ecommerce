from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name',"last_name" ,"username",'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control rounded border-success'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control rounded border-success'})
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control rounded border-success'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control rounded border-success'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control rounded border-success'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control rounded border-success'})


