import xlwt
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.forms import BaseInlineFormSet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, FormView, ListView, UpdateView
from django_filters.views import FilterView
from extra_views import (
    CreateWithInlinesView,
    InlineFormSetFactory,
    NamedFormsetsMixin,
    UpdateWithInlinesView,
)

from apps.core.mixins import SuccessURLMixin
from apps.responses.models import Answer, OpenResponse, RegionalResponse

from .filters import OpenResponseFilter, RegionalResponseFilter
from .forms import *
from .models import *


class SurveyListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "surveys/survey_list.html"
    model = Survey
    permission_required = ["surveys.view_survey"]

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Survey.objects.all()
            .select_related("client", "city", "regionalsurvey", "opensurvey")
            .prefetch_related(
                "responses",
            )
            .annotate(num_responses=Count("responses"))
        )

        if user.groups.filter(name="Entrevistadores").exists():
            u_surveys = user.surveys.values_list("survey", flat=True)
            queryset = queryset.filter(pk__in=u_surveys, finalized=False)
        if user.client:
            queryset = queryset.filter(client=user.client)

        return queryset.order_by("-creation_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class QuestionInline(InlineFormSetFactory):
    model = Question
    form_class = QuestionForm
    factory_kwargs = {"extra": 0}


class QuestionOrderedInline(InlineFormSetFactory):
    model = Question
    form_class = OrderedQuestionForm
    factory_kwargs = {"extra": 0, "can_delete": False}


class SurveyInterviewerInline(InlineFormSetFactory):
    model = SurveyInterviewer
    form_class = SurveyInterviewerForm
    factory_kwargs = {"extra": 0}
    initial = {"teste": "teste"}


class CustomInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop("survey", None)
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["survey"] = self.instance
        return kwargs


class RegionalSurveyInterviewerInline(InlineFormSetFactory):
    model = RegionalSurveyInterviewer
    form_class = RegionalSurveyInterviewerForm
    formset_class = CustomInlineFormSet
    factory_kwargs = {"extra": 0}

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs["survey"] = self.object
        return kwargs


class OpenSurveyCreateView(
    LoginRequiredMixin,
    NamedFormsetsMixin,
    PermissionRequiredMixin,
    SuccessURLMixin,
    CreateWithInlinesView,
):
    model = OpenSurvey
    inlines = [QuestionInline]
    inlines_names = ["Questions"]
    fields = [
        "name",
        "slug",
        "client",
        "city",
        "header",
        "bg_color",
        "max_responses",
        "open_form",
    ]
    permission_required = ["surveys.add_survey"]
    success_url = "surveys:open_update"
    success_url_new = "surveys:open_create"
    success_url_close = "surveys:list"


class OpenSurveyUpdateView(
    LoginRequiredMixin,
    NamedFormsetsMixin,
    PermissionRequiredMixin,
    SuccessURLMixin,
    UpdateWithInlinesView,
):
    model = OpenSurvey
    inlines = [QuestionInline]
    inlines_names = ["Questions"]
    fields = [
        "name",
        "slug",
        "client",
        "city",
        "header",
        "bg_color",
        "max_responses",
        "open_form",
    ]
    permission_required = ["surveys.change_survey"]
    success_url = "surveys:open_update"
    success_url_new = "surveys:open_create"
    success_url_close = "surveys:list"


class RegionalSurveyCreateView(
    LoginRequiredMixin,
    NamedFormsetsMixin,
    PermissionRequiredMixin,
    SuccessURLMixin,
    CreateWithInlinesView,
):
    model = RegionalSurvey
    inlines = [QuestionInline]
    inlines_names = ["Questions"]
    fields = ["name", "client", "city", "no_neigh", "enumerated"]
    permission_required = ["surveys.add_survey"]
    success_url = "surveys:regional_update"
    success_url_new = "surveys:regional_create"
    success_url_close = "surveys:list"


class RegionalSurveyUpdateView(
    LoginRequiredMixin,
    NamedFormsetsMixin,
    PermissionRequiredMixin,
    SuccessURLMixin,
    UpdateWithInlinesView,
):
    model = RegionalSurvey
    inlines = [QuestionInline]
    inlines_names = ["Questions"]
    fields = ["name", "client", "city", "no_neigh", "finalized", "enumerated"]
    permission_required = ["surveys.change_survey"]
    template_name = "surveys/regionalsurvey_update.html"
    success_url = "surveys:regional_update"
    success_url_new = "surveys:regional_create"
    success_url_close = "surveys:list"


class RegionalSurveyUpdateInterviewersView(
    LoginRequiredMixin,
    NamedFormsetsMixin,
    PermissionRequiredMixin,
    SuccessURLMixin,
    UpdateWithInlinesView,
):
    model = RegionalSurvey
    inlines = [RegionalSurveyInterviewerInline]
    inlines_names = ["Interviewers"]
    fields = ["name"]
    permission_required = ["surveys.change_survey"]
    template_name = "surveys/regionalsurvey_interviewers.html"
    success_url = "surveys:regional_interviewers"
    success_url_new = "surveys:regional_create"
    success_url_close = "surveys:list"


class RegionalSurveyMetaView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = RegionalSurvey
    context_object_name = "survey"
    template_name = "surveys/regionalsurvey_meta.html"
    permission_required = ["responses.add_response"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        survey = self.get_object()
        meta = survey.meta
        responses = list(
            RegionalResponse.objects.filter(survey=survey).values(
                "sector", "neighborhood", "gender", "age_group"
            )
        )
        sectors = survey.city.sectors.values_list("pk", flat=True)

        if user.groups.filter(name="Entrevistadores").exists():
            sectors = (
                user.surveys.filter(survey=survey)
                .values_list("regionalsurveyinterviewer__sectors", flat=True)
                .distinct()
            )
            del_sectors = []
            for sector in meta["sectors"]:
                if int(sector) not in sectors:
                    del_sectors.append(sector)
            for sector in del_sectors:
                del meta["sectors"][sector]

        for sector in meta["sectors"]:
            for gender in meta["sectors"][sector]["genders"]:
                meta["sectors"][sector]["genders"][gender]["responses"] = len(
                    [
                        response
                        for response in responses
                        if response["sector"] == int(sector)
                        and response["gender"] == int(gender)
                    ]
                )
            for age_group in meta["sectors"][sector]["age_groups"]:
                meta["sectors"][sector]["age_groups"][age_group]["responses"] = len(
                    [
                        response
                        for response in responses
                        if response["sector"] == int(sector)
                        and response["age_group"] == int(age_group)
                    ]
                )
            for neigh in meta["sectors"][sector]["neighborhoods"]:
                meta["sectors"][sector]["neighborhoods"][neigh]["responses"] = len(
                    [
                        response
                        for response in responses
                        if response["neighborhood"] == int(neigh)
                    ]
                )

        context["meta"] = meta
        return context


class SurveyOrderedView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateWithInlinesView
):
    model = Survey
    inlines = [QuestionOrderedInline]
    fields = []
    success_url = reverse_lazy("surveys:list")
    permission_required = ["surveys.change_survey"]
    template_name = "surveys/ordered_survey_form.html"


class SurveyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Survey
    permission_required = ["surveys.delete_survey"]
    success_url = reverse_lazy("surveys:list")


class MetaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = "surveys/meta_update.html"
    model = RegionalSurvey
    fields = ["name"]
    permission_required = ["surveys.change_survey"]

    def post(self, request, *args, **kwargs):
        survey = self.get_object()
        survey.meta = survey.city.generate_meta()
        survey.max_responses = survey.city.max_responses()
        survey.save()
        messages.add_message(
            self.request, messages.SUCCESS, "Metas atualizadas com sucessso"
        )
        return redirect(reverse_lazy("surveys:list"))


class RegionalSurveyResultView(LoginRequiredMixin, PermissionRequiredMixin, FilterView):
    model = RegionalResponse
    filterset_class = RegionalResponseFilter
    template_name = "surveys/regionalsurvey_results.html"
    permission_required = ["responses.view_response"]

    def get_queryset(self, **kwargs):
        survey_pk = self.kwargs["pk"]
        survey = RegionalSurvey.objects.get(id=survey_pk)
        return RegionalResponse.objects.filter(survey=survey)

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        survey_pk = self.kwargs["pk"]
        survey = RegionalSurvey.objects.get(id=survey_pk)
        kwargs["extra"] = {"city": survey.city, "survey": survey}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey_pk = self.kwargs["pk"]
        survey = RegionalSurvey.objects.get(id=survey_pk)
        queryset = self.get_queryset()
        context["survey"] = survey
        context["questions"] = survey.questions.filter(published=True)
        context["answers"] = list(
            Answer.objects.filter(response__in=queryset).values(
                "question", "body", "response"
            )
        )
        context["sectors"] = survey.city.sectors.values("id", "name")
        return context


class OpenSurveyResultView(LoginRequiredMixin, PermissionRequiredMixin, FilterView):
    model = OpenResponse
    filterset_class = OpenResponseFilter
    template_name = "surveys/opensurvey_results.html"
    permission_required = ["responses.view_response"]

    def get_queryset(self, **kwargs):
        survey_pk = self.kwargs["pk"]
        survey = OpenSurvey.objects.get(id=survey_pk)
        return OpenResponse.objects.filter(survey=survey)

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        survey_pk = self.kwargs["pk"]
        survey = OpenSurvey.objects.get(id=survey_pk)
        kwargs["extra"] = {"survey": survey}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey_pk = self.kwargs["pk"]
        survey = OpenSurvey.objects.get(id=survey_pk)
        queryset = self.get_queryset()
        context["survey"] = survey
        context["questions"] = survey.questions.all()
        context["answers"] = list(
            Answer.objects.filter(response__in=queryset).values(
                "question", "body", "response"
            )
        )
        return context


class QuestionModifyView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = QuestionModifyForm
    template_name = "surveys/question_modify.html"
    permission_required = ["surveys.change_survey"]

    def get_question(self):
        question_pk = self.kwargs["pk"]
        question = Question.objects.get(pk=question_pk)
        return question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_question()
        context["question"] = question
        context["answers"] = list(
            question.answers.values("question", "body", "response")
        )
        return context

    def form_valid(self, form):
        question = self.get_question()
        find = form.data["find"]
        replace = form.data["replace"]
        answers = Answer.objects.filter(question=question, body=find)

        for answer in answers:
            answer.body = replace
            answer.save()

        if answers.count() > 0:
            messages.add_message(
                self.request, messages.SUCCESS, "Respostas alteradas com sucesso"
            )
        else:
            messages.add_message(
                self.request,
                messages.WARNING,
                "Nenhuma resposta continha as palavras informadas",
            )
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("surveys:question_modify", kwargs={"pk": self.kwargs["pk"]})


class QuestionSectorView(LoginRequiredMixin, FilterView):
    model = RegionalResponse
    filterset_class = RegionalResponseFilter
    template_name = "surveys/question_sector.html"

    def get_question(self):
        question_pk = self.kwargs["pk"]
        question = Question.objects.get(pk=question_pk)
        return question

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        question = self.get_question()
        survey = question.survey
        kwargs["extra"] = {"city": survey.city, "survey": survey}
        return kwargs

    def get_queryset(self, **kwargs):
        question = self.get_question()
        survey = question.survey
        return RegionalResponse.objects.filter(survey=survey)

    def get(self, request, *args, **kwargs):
        question = self.get_question()
        sectors = question.survey.city.sectors.values("id", "name")
        filter = self.get_filterset(self.get_filterset_class())
        answers = list(
            Answer.objects.filter(response__in=filter.qs).values(
                "question", "body", "response"
            )
        )

        context = {
            "question": question,
            "sectors": sectors,
            "responses": filter.qs,
            "answers": answers,
        }

        data = dict()
        data["chart"] = render_to_string(self.template_name, context, request=request)
        return JsonResponse(data)


class QuestionCompareView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "surveys/question_compare.html"

    def get(self, request, *args, **kwargs):
        sector = None
        if "sector" in self.request.GET:
            sector = int(self.request.GET.get("sector"))

        context = {"question": self.get_object(), "sector": sector}

        data = dict()
        data["chart"] = render_to_string(self.template_name, context, request=request)
        return JsonResponse(data)


class QuestionSplitView(LoginRequiredMixin, FilterView):
    model = RegionalResponse
    filterset_class = RegionalResponseFilter
    template_name = "surveys/question_split.html"

    def get_question(self):
        question_pk = self.kwargs["pk"]
        question = Question.objects.get(pk=question_pk)
        return question

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        question = self.get_question()
        survey = question.survey
        kwargs["extra"] = {"city": survey.city, "survey": survey}
        return kwargs

    def get(self, request, *args, **kwargs):
        question = self.get_question()
        filter = self.get_filterset(self.get_filterset_class())
        answers = question.answers.filter(response__in=filter.qs)

        final = {}
        series = []

        for answer in answers:
            items = answer.body.split(",")
            for item in items:
                if item:
                    if item[0] == " ":
                        item = item[1:]
                    if item[-1] == " ":
                        item = item[:-1]

                    item = item.lower()

                    if item in final:
                        final[item] += 1
                    else:
                        final[item] = 1

        total = 0

        for key in final:
            series.append({"name": key, "y": final[key]})
            total += final[key]

        series = sorted(series, key=lambda k: k["name"])

        for i in range(len(series)):
            value = series[i]["y"]
            percentage = round((value * 100) / total, 2)
            series[i]["y"] = percentage
            series[i]["value"] = value

        context = {
            "question": question,
            "series": series,
            "height": len(series) * 40 + 100,
        }

        data = dict()
        data["chart"] = render_to_string(self.template_name, context, request=request)
        return JsonResponse(data)


def export_survey_xls(request, pk):
    survey = RegionalSurvey.objects.get(pk=pk)
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="{}.xls"'.format(
        survey.city.name
    )

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet(survey.city.name)
    font_style = xlwt.XFStyle()

    index = 0

    row = (
        ["Setor", "Bairro", "Gênero", "Idade"]
        + [question.text for question in survey.questions.all()]
        + ["Entrevistadora", "Número de controle"]
    )
    for col in range(len(row)):
        ws.write(index, col, row[col], font_style)

    responses = (
        RegionalResponse.objects.filter(survey=survey)
        .select_related("sector", "neighborhood")
        .prefetch_related("answers")
    )
    for res in responses:
        row = [
            res.sector.name,
            res.neighborhood.name if res.neighborhood else "",
            res.get_gender_display(),
            res.get_age_group_display(),
        ]
        for answer in res.answers.order_by("question"):
            row = row + [answer.body.replace("[", "").replace("]", "").replace("'", "")]
            row = row + [res.interviewer, res.control_number]
        index = index + 1
        for col in range(len(row)):
            ws.write(index, col, row[col], font_style)

    wb.save(response)
    return response
