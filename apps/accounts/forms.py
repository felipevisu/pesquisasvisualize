from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django import forms

from .models import User


class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type', 'client']

    def clean(self):
        data = super().clean()
        user_type = data.get('user_type')
        client = data.get('client')

        if user_type == User.CLIENT and client is None:
            self.add_error('client', 'Este tipo de usuário precisa estar vinculado a um cliente')

        if user_type != User.CLIENT and client:
            self.add_error('client', 'Este tipo de usuário não pode estar vinculado a um cliente')


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type' ,'client']