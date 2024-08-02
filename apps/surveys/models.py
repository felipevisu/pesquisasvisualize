from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField

from apps.locations.models import City
from apps.responses.models import RegionalResponse


class Survey(models.Model):
    name = models.CharField("nome", max_length=200)
    slug = models.SlugField("atalho", unique=True, null=True, blank=True)
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="surveys",
        verbose_name="cliente",
    )
    city = models.ForeignKey(
        City,
        related_name="surveys",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="cidade",
    )
    creation_date = models.DateTimeField("data de criação", auto_now_add=True)
    finalized = models.BooleanField(
        "finalizado",
        default=False,
        help_text="A pesquisa finalizada não estará mais disponível para as entrevistadoras",
    )
    enumerated = models.BooleanField(
        "enumerada",
        default=False,
        help_text="Para pesquisas feitas no papel enumerado o número de série de cada questionário deverá ser informado",
    )

    class Meta:
        ordering = ["-creation_date"]
        verbose_name = "Pesquisa"
        verbose_name_plural = "Pesquisas"

    def __str__(self):
        return self.name

    def total_questions(self):
        return self.questions.count()

    def total_responses(self):
        return self.responses.count()


class RegionalSurvey(Survey):
    max_responses = models.PositiveIntegerField("número de formulários", default=1)
    no_neigh = models.BooleanField("pesquisa sem bairros", default=False)
    meta = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Pesquisa regional"
        verbose_name_plural = "Pesquisas regionais"

    def save(self):
        if not self.pk:
            self.max_responses = self.city.max_responses()
            self.meta = self.city.generate_meta()
        super().save()

    def get_progress(self):
        return int(self.total_responses() * 100 / self.max_responses)


class OpenSurvey(Survey):
    max_responses = models.PositiveIntegerField(
        "número de formulários", null=True, blank=True
    )
    open_form = models.BooleanField("formulário aberto ao público", default=False)
    header = models.FileField("cabeçalho", null=True, blank=True, upload_to="open")
    bg_color = models.CharField(
        "cor do fundo", max_length=50, null=True, blank=True, default="#007BFF"
    )

    class Meta:
        verbose_name = "Pesquisa aberta"
        verbose_name_plural = "Pesquisas abertas"


class Question(models.Model):
    PIE = "pie"
    COLUMN = "column"
    LIST = "list"

    CHART = ((PIE, "pizza"), (COLUMN, "coluna"), (LIST, "lista"))

    TEXT = "text"
    RADIO = "radio"
    SELECT = "select"
    SELECT_MULTIPLE = "select-multiple"
    NUMERIC = "numeric"

    TYPES = (
        (TEXT, "text"),
        (RADIO, "radio"),
        (SELECT, "select"),
        (SELECT_MULTIPLE, "select multiple"),
        (NUMERIC, "numeric"),
    )

    survey = models.ForeignKey(
        Survey,
        related_name="questions",
        on_delete=models.CASCADE,
        verbose_name="pesquisa",
    )
    text = models.CharField("texto", max_length=200)
    required = models.BooleanField("obrigatório", default=True)
    key = models.SlugField("chave", null=True, blank=True, max_length=100)
    question_type = models.CharField(
        "tipo de questão", max_length=25, choices=TYPES, default=RADIO
    )
    chart_type = models.CharField(
        "tipo de gráfico", max_length=25, choices=CHART, default=PIE
    )
    choices = models.TextField(
        "opções", blank=True, null=True, help_text="Utilize ';' para separar as opções"
    )
    order = models.PositiveIntegerField("ordem", default=1)
    published = models.BooleanField("publicada", default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return self.text

    def clean(self, *args, **kwargs):
        super(Question, self).clean(*args, **kwargs)

        if self.question_type in [
            Question.RADIO,
            Question.SELECT,
            Question.SELECT_MULTIPLE,
        ]:
            values = self.choices.split(";")
            if len(values) < 2:
                raise ValidationError({"choices": "Informe pelo menos duas opções"})

    def get_choices(self):
        choices = self.choices.split(";")
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c, c))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def get_choices_list(self):
        choices = self.choices.split(";")
        choices_list = []
        for c in choices:
            choices_list.append(c.strip())
        return choices_list


class SurveyInterviewer(models.Model):
    interviewer = models.ForeignKey(
        "accounts.User",
        related_name="surveys",
        verbose_name="entrevistadora",
        on_delete=models.CASCADE,
    )
    survey = models.ForeignKey(
        Survey,
        related_name="interviewers",
        verbose_name="pesquisa",
        on_delete=models.CASCADE,
    )
    creation_date = models.DateTimeField("data de criação", auto_now_add=True)


class RegionalSurveyInterviewer(SurveyInterviewer):
    sectors = models.ManyToManyField(
        "locations.Sector", verbose_name="setores", blank=True
    )
