import uuid

from django import forms
from django.utils.safestring import mark_safe

from apps.locations.models import City, Neighborhood, Sector
from apps.surveys.models import Question

from .models import *


def save_answers(items, response):
    for field_name, field_value in items:
        if field_name.startswith("question_"):
            q_id = int(field_name.split("_")[1])
            q = Question.objects.get(pk=q_id)
            a = Answer(question=q, body=field_value)
            a.response = response
            a.save()


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = []

    def get_question_fields(self):
        fields = []
        for item in self:
            if item.name.startswith("question_"):
                fields.append(item)
        return fields

    def __init__(self, survey, *args, **kwargs):
        self.survey = survey
        self.uuid = random_uuid = uuid.uuid4().hex
        super(ResponseForm, self).__init__(*args, **kwargs)

        data = kwargs.get("data")

        for q in survey.questions.filter(published=True):
            if q.question_type == Question.TEXT:
                self.fields["question_%d" % q.pk] = forms.CharField(label=q.text)
            elif q.question_type == Question.RADIO:
                question_choices = q.get_choices()
                self.fields["question_%d" % q.pk] = forms.ChoiceField(
                    label=q.text, widget=forms.RadioSelect, choices=question_choices
                )
            elif q.question_type == Question.SELECT:
                question_choices = q.get_choices()
                question_choices = tuple([("", "-------------")]) + question_choices
                self.fields["question_%d" % q.pk] = forms.ChoiceField(
                    label=q.text, widget=forms.Select, choices=question_choices
                )
            elif q.question_type == Question.SELECT_MULTIPLE:
                question_choices = q.get_choices()
                self.fields["question_%d" % q.pk] = forms.MultipleChoiceField(
                    label=q.text,
                    widget=forms.CheckboxSelectMultiple,
                    choices=question_choices,
                )
            elif q.question_type == Question.NUMERIC:
                self.fields["question_%d" % q.pk] = forms.DecimalField(label=q.text)

            if q.required:
                self.fields["question_%d" % q.pk].required = True
                self.fields["question_%d" % q.pk].widget.attrs["class"] = "required"
            else:
                self.fields["question_%d" % q.pk].required = False

            if data:
                self.fields["question_%d" % q.pk].initial = data.get(
                    "question_%d" % q.pk
                )


class OpenResponseForm(ResponseForm):

    class Meta:
        model = OpenResponse
        fields = []

    def save(self, commit=True):
        response = super(ResponseForm, self).save(commit=False)
        response.survey = self.survey
        response.interview_uuid = self.uuid
        response.save()
        save_answers(self.cleaned_data.items(), response)
        return response


class RegionalResponseForm(ResponseForm):

    class Meta:
        model = RegionalResponse
        fields = ["sector", "neighborhood", "gender", "age_group", "control_number"]

    def __init__(self, survey, user, *args, **kwargs):
        super(RegionalResponseForm, self).__init__(survey, *args, **kwargs)

        city = survey.city
        sectors = Sector.objects.select_related("city").filter(city=city)
        neighborhoods = Neighborhood.objects.select_related(
            "sector", "sector__city"
        ).filter(sector__city=city)

        if user.groups.filter(name="Entrevistadores").exists():
            sectors_list = user.surveys.all().values_list(
                "regionalsurveyinterviewer__sectors", flat=True
            )
            sectors = sectors.filter(pk__in=sectors_list)
            neighborhoods = neighborhoods.filter(sector__in=sectors)

        self.survey = survey
        self.fields["sector"].queryset = sectors
        self.fields["neighborhood"].queryset = neighborhoods

        if not survey.no_neigh:
            self.fields["neighborhood"].required = True

        if survey.enumerated:
            self.fields["control_number"].required = True

    def clean(self):
        data = super().clean()
        survey = self.survey
        meta = survey.meta

        sector = data.get("sector")
        neighborhood = data.get("neighborhood")
        gender = data.get("gender")
        age_group = data.get("age_group")

        responses = RegionalResponse.objects.filter(survey=survey)

        if sector and neighborhood:
            if sector.n_responses:
                count = responses.filter(sector=sector).count()
                if count >= meta["sectors"][str(sector.pk)]["total"]:
                    self.add_error(
                        "sector", "Esta setor já preencheu todos os questionários"
                    )

            if neighborhood not in sector.neighborhoods.all():
                self.add_error(
                    "neighborhood", "Este bairro não pertence ao setor selecionado"
                )

        if neighborhood and not sector.n_responses:
            count = responses.filter(neighborhood=neighborhood).count()
            try:
                if (
                    count
                    >= meta["sectors"][str(sector.pk)]["neighborhoods"][
                        str(neighborhood.pk)
                    ]["surveys"]
                ):
                    self.add_error(
                        "neighborhood",
                        "Este bairro já preencheu todos os questionários",
                    )
            except KeyError:
                self.add_error(
                    "neighborhood",
                    "Este bairro não consta nas metas para esta pesquisa",
                )

        if gender and sector:
            count = responses.filter(gender=gender, sector=sector).count()
            if (
                count
                >= meta["sectors"][str(sector.pk)]["genders"][str(gender)]["surveys"]
            ):
                self.add_error(
                    "gender", "Este sexo já preencheu todos os questionários"
                )

        if age_group and sector:
            count = responses.filter(age_group=age_group, sector=sector).count()
            if (
                count
                >= meta["sectors"][str(sector.pk)]["age_groups"][str(age_group)][
                    "surveys"
                ]
            ):
                self.add_error(
                    "age_group",
                    "Esta faixa etária já preencheu todos os questionários neste setor",
                )

    def save(self, commit=True):
        response = super(RegionalResponseForm, self).save(commit=False)
        response.survey = self.survey
        response.city = self.survey.city
        response.interview_uuid = self.uuid
        response.interviewer = self.interviewer
        response.save()
        save_answers(self.cleaned_data.items(), response)
        return response
