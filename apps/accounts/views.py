from django.contrib.auth.forms import PasswordResetForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.models import Group
from apps.core.mixins import SuccessURLMixin

from .forms import UserAdminCreationForm, UserAdminForm
from .models import User


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    paginate_by = 20
    permission_required = ['accounts.view_user']


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessURLMixin, CreateView):
    model = User
    form_class = UserAdminCreationForm
    permission_required = ['accounts.add_user']
    success_url = 'accounts:update'
    success_url_new = 'accounts:create'
    success_url_close = 'accounts:list'

    def form_valid(self, form):
        user = form.save()

        if form.instance.user_type == 'client':
            user.groups.add(Group.objects.get(name='Clientes'))
        if form.instance.user_type == 'administrator':
            user.groups.add(Group.objects.get(name='Administradores'))
        if form.instance.user_type == 'interviewer':
            user.groups.add(Group.objects.get(name='Entrevistadores'))

        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessURLMixin, UpdateView):
    model = User
    form_class = UserAdminForm
    permission_required = ['accounts.change_user']
    success_url = 'accounts:update'
    success_url_new = 'accounts:create'
    success_url_close = 'accounts:list'


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = ['accounts.delete_user']
    success_url = reverse_lazy('accounts:list')


class PasswordChangeView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'registration/password_change_form.html'
    permission_required = ['accounts.change_user']
    form_class = SetPasswordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        return kwargs

    def get_success_url(self):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        return reverse_lazy('accounts:update', kwargs={'pk': user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        return context
