from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect

class SuccessURLMixin:
    success_message = None

    def get_success_url(self):
        if self.success_message:
            success = self.success_message
        else:
            success = "Item '{}: {}' salvo com sucesso".format(self.model._meta.verbose_name, self.object)
        messages.add_message(self.request, messages.SUCCESS, success)

        kwargs = {}
        kwargs.update(self.get_url_kwargs())

        if 'addanother' in self.request.POST:
            url = self.success_url_new
        elif 'close' in self.request.POST:
            url = self.success_url_close
            if 'parent' in kwargs:
                kwargs['pk'] = kwargs['parent']
                del kwargs['parent']
        else:
            url = self.success_url
            kwargs['pk'] = self.object.pk

        url = reverse_lazy(url, kwargs=kwargs)

        print(url)

        if 'page' in self.request.GET and 'close' in self.request.POST:
            url += '?page=' + self.request.GET.get('page')

        return url

    def get_url_kwargs(self):
        return {}


class DeleteURLMixin:
    success_message = None

    def get_success_url(self):
        if self.success_message:
            success = self.success_message
        else:
            success = "Item '{}: {}' excluido com sucesso".format(self.model._meta.verbose_name, self.object)
        messages.add_message(self.request, messages.SUCCESS, success)

        kwargs = {}
        kwargs.update(self.get_url_kwargs())
        
        return reverse_lazy(self.success_url, kwargs=kwargs)

    def get_url_kwargs(self):
        return {}