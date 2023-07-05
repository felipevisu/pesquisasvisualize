from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.surveys.models import Question


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    