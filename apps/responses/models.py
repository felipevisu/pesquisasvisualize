from django.core.exceptions import ValidationError
from django.db import models
from django_random_queryset import RandomManager

from apps.locations.models import City, Neighborhood, Sector


class Response(models.Model):
    interview_uuid = models.CharField("Identificador", max_length=36)
    interviewer = models.CharField(
        "Entrevistador", max_length=36, null=True, blank=True
    )
    creation_date = models.DateTimeField("data de criação", auto_now_add=True)
    modification_date = models.DateTimeField("data de modificação", auto_now=True)
    survey = models.ForeignKey(
        "surveys.Survey",
        on_delete=models.PROTECT,
        related_name="responses",
        verbose_name="pesquisa",
    )
    control_number = models.CharField(
        "Número de controle",
        max_length=10,
        blank=True,
        null=True,
        help_text="Para idenficar a versão física em pesquisas enumeradas",
    )

    objects = RandomManager()

    class Meta:
        ordering = ["-creation_date"]

    def __str__(self):
        return "Entrevista %s" % self.interview_uuid


class OpenResponse(Response):

    class Meta:
        verbose_name = "Entrevista aberta"
        verbose_name_plural = "Entrevistas abertas"


class RegionalResponse(Response):
    MALE = 1
    FEMALE = 2

    AGE_1 = 1
    AGE_2 = 2
    AGE_3 = 3
    AGE_4 = 4
    AGE_5 = 5

    GENDER = ((MALE, "Masculino"), (FEMALE, "Feminino"))

    AGE_GROUP = (
        (AGE_1, "16 a 24"),
        (AGE_2, "25 a 34"),
        (AGE_3, "35 a 44"),
        (AGE_4, "45 a 60"),
        (AGE_5, "Acima de 60"),
    )

    city = models.ForeignKey(
        City, verbose_name="cidade", related_name="responses", on_delete=models.PROTECT
    )
    sector = models.ForeignKey(
        Sector, verbose_name="setor", related_name="responses", on_delete=models.PROTECT
    )
    neighborhood = models.ForeignKey(
        Neighborhood,
        verbose_name="bairro",
        related_name="responses",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    gender = models.PositiveIntegerField("gênero", choices=GENDER)
    age_group = models.PositiveIntegerField("faixa etária", choices=AGE_GROUP)

    class Meta:
        verbose_name = "Entrevista regional"
        verbose_name_plural = "Entrevistas regionais"


class Answer(models.Model):
    response = models.ForeignKey(
        Response,
        verbose_name="entrevista",
        related_name="answers",
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        "surveys.Question",
        verbose_name="pergunta",
        related_name="answers",
        on_delete=models.PROTECT,
    )
    creation_date = models.DateTimeField("data de criação", auto_now_add=True)
    modification_date = models.DateTimeField("data de modificação", auto_now=True)
    body = models.TextField("resposta", blank=True, null=True)

    class Meta:
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"
