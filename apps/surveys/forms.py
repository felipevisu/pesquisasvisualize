from django import forms

from apps.accounts.models import User
from apps.locations.models import Sector

from .models import *


class QuestionModifyForm(forms.Form):
    find = forms.CharField(label="Encontrar", required=False)
    replace = forms.CharField(label="Substituir")


class RegionalSurveyForm(forms.ModelForm):
    class Meta:
        model = RegionalSurvey
        fields = ["name", "city"]


class OpenSurveyForm(forms.ModelForm):
    class Meta:
        model = OpenSurvey
        fields = ["name", "open_form", "max_responses"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "text",
            "required",
            "question_type",
            "chart_type",
            "choices",
            "key",
            "order",
        ]
        widgets = {
            "order": forms.HiddenInput(),
        }


class RegionalSurveyInterviewerForm(forms.ModelForm):
    interviewer = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="Entrevistadores"),
        label="Entrevistador(a)",
    )
    sectors = forms.ModelMultipleChoiceField(
        queryset=Sector.objects.all(),
        label="Setores",
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = RegionalSurveyInterviewer
        fields = ["interviewer", "sectors"]

    def __init__(self, *args, **kwargs):
        survey = kwargs.pop("survey", None)
        super().__init__(*args, **kwargs)
        if survey:
            self.fields["sectors"].queryset = Sector.objects.filter(city=survey.city)


class SurveyInterviewerForm(forms.ModelForm):
    interviewer = forms.ModelChoiceField(
        queryset=User.objects.all(), label="Entrevistador(a)"
    )

    class Meta:
        model = SurveyInterviewer
        fields = ["interviewer"]


class OrderedQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["order"]
        widgets = {
            "order": forms.HiddenInput(),
        }
