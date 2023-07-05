from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from apps.surveys.models import OpenSurvey, RegionalSurvey

from .forms import OpenResponseForm, RegionalResponseForm
from .models import OpenResponse, RegionalResponse


class OpenResponseSuccessView(TemplateView):
    model = OpenResponse
    template_name = 'responses/openresponse_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["survey"] = OpenSurvey.objects.get(slug=self.kwargs['slug'])
        return context
    

class OpenResponseOpenCreateView(CreateView):
    model = OpenResponse
    form_class = OpenResponseForm
    template_name = 'responses/openresponse_open_form.html'

    def get_form_kwargs(self):
        survey_slug = self.kwargs['slug']
        survey = OpenSurvey.objects.get(slug=survey_slug)
        kwargs = super().get_form_kwargs()
        kwargs.update({'survey': survey})
        return kwargs

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Questionário enviado com sucessso')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Não foi possível enviar o questionário')
        return super().form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('open:open_success', kwargs={'slug': self.kwargs['slug']})


class OpenResponseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = OpenResponse
    form_class = OpenResponseForm
    permission_required = ['responses.add_response']

    def get_form_kwargs(self):
        survey_pk = self.kwargs['pk']
        survey = OpenSurvey.objects.get(pk=survey_pk)
        kwargs = super().get_form_kwargs()
        kwargs.update({'survey': survey})
        return kwargs

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Questionário enviado com sucessso')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Não foi possível enviar o questionário')
        return super().form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('responses:open_create', kwargs={'pk': self.kwargs['pk']})


class RegionalResponseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = RegionalResponse
    form_class = RegionalResponseForm
    permission_required = ['responses.add_response']

    def get_form_kwargs(self):
        survey_pk = self.kwargs['pk']
        survey = RegionalSurvey.objects.get(pk=survey_pk)
        user = self.request.user
        kwargs = super().get_form_kwargs()
        kwargs.update({'survey': survey, 'user': user})
        return kwargs

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Questionário enviado com sucessso')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Não foi possível enviar o questionário')
        return super().form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('responses:regional_create', kwargs={'pk': self.kwargs['pk']})
