from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.http import HttpResponseRedirect

from apps.core.mixins import SuccessURLMixin

from .models import Client


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    paginate_by = 20
    permission_required = ['clients.view_client']

    def get_queryset(self):
        return Client.objects.annotate(n_surveys=Count('surveys', distinct=True), n_responses=Count('surveys__responses'))


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessURLMixin, CreateView):
    model = Client
    fields = ['name']
    permission_required = ['clients.add_client']
    success_url = 'clients:update'
    success_url_new = 'clients:create'
    success_url_close = 'clients:list'


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessURLMixin, UpdateView):
    model = Client
    fields = ['name']
    permission_required = ['clients.change_client']
    success_url = 'clients:update'
    success_url_new = 'clients:create'
    success_url_close = 'clients:list'


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = ['clients.delete_client']
    success_url = reverse_lazy('clients:list')
