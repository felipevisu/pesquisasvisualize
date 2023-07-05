from django.db import models
from django.core.exceptions import ValidationError
import json


class City(models.Model):
    name = models.CharField('nome da cidade', max_length=200)

    n_male = models.DecimalField('porcentagem de homemes', max_digits=5, decimal_places=2, default=0)
    n_female = models.DecimalField('porcentagem de mulheres', max_digits=5, decimal_places=2, default=0)

    age_group_1 = models.DecimalField('16 a 24 anos', max_digits=5, decimal_places=2, default=0)
    age_group_2 = models.DecimalField('25 a 34 anos', max_digits=5, decimal_places=2, default=0)
    age_group_3 = models.DecimalField('35 a 44 anos', max_digits=5, decimal_places=2, default=0)
    age_group_4 = models.DecimalField('45 a 59 anos', max_digits=5, decimal_places=2, default=0)
    age_group_5 = models.DecimalField('acima de 60 anos', max_digits=5, decimal_places=2, default=0)


    class Meta:
        ordering = ['name']
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    def __str__(self):
        return self.name

    def max_responses(self):
        total = 0
        for sector in self.sectors.all():
            total += sector.max_responses()
        return total

    def generate_meta(self):
        meta = {
            'genders': self.get_gender_surveys(),
            'age_groups': self.get_age_surveys(),
            'sectors': []
        }
        sectors = {}
        for sector in self.sectors.all():
            sec = sector.generate_meta()
            sec['pk'] =  sector.pk
            sec['name'] = sector.name
            sectors[sector.pk] = sec
        meta['sectors'] = sectors
        return meta

    def get_gender_surveys(self):
        total = self.max_responses()
        values = [round((total*self.n_male)/100), round((total*self.n_female)/100)]
        while(sum(values) != total):
            if sum(values) > total:
                i = values.index(max(values))
                values[i] -= 1
            else:
                i = values.index(min(values))
                values[i] += 1
        response = {
            '1': {'name': 'Homens', 'value': float(self.n_male), 'surveys': values[0]},
            '2': {'name': 'Mulheres', 'value': float(self.n_female), 'surveys': values[1]},
        }
        return response

    def get_age_surveys(self):
        total = self.max_responses()
        values = [
            round((total*self.age_group_1)/100),
            round((total*self.age_group_2)/100),
            round((total*self.age_group_3)/100),
            round((total*self.age_group_4)/100),
            round((total*self.age_group_5)/100),
        ]
        while(sum(values) != total):
            if sum(values) > total:
                i = values.index(max(values))
                values[i] -= 1
            else:
                i = values.index(min(values))
                values[i] += 1
        response = {
            '1': {'name': '16 a 24 anos', 'value': float(self.age_group_1), 'surveys': values[0]},
            '2': {'name': '25 a 34 anos', 'value': float(self.age_group_2), 'surveys': values[1]},
            '3': {'name': '35 a 44 anos', 'value': float(self.age_group_3), 'surveys': values[2]},
            '4': {'name': '45 a 60 anos', 'value': float(self.age_group_4), 'surveys': values[3]},
            '5': {'name': 'Acima de 60 anos', 'value': float(self.age_group_5), 'surveys': values[4]},
        }
        return response

    max_responses.short_description = "questionários"
    get_gender_surveys.short_description = "divisão por sexo (M|F)"
    get_age_surveys.short_description = "divisão por faixa etária"


class Sector(models.Model):
    name = models.CharField('nome do setor', max_length=200)
    n_responses = models.PositiveIntegerField('número de questionários', null=True, blank=True)
    city = models.ForeignKey(City, related_name='sectors', verbose_name='cidade', on_delete=models.CASCADE)

    n_male = models.PositiveIntegerField('porcentagem de homemes', null=True, blank=True)
    n_female = models.PositiveIntegerField('porcentagem de mulheres', null=True, blank=True)

    age_group_1 = models.PositiveIntegerField('16 a 24 anos', null=True, blank=True)
    age_group_2 = models.PositiveIntegerField('25 a 34 anos', null=True, blank=True)
    age_group_3 = models.PositiveIntegerField('35 a 44 anos', null=True, blank=True)
    age_group_4 = models.PositiveIntegerField('45 a 59 anos', null=True, blank=True)
    age_group_5 = models.PositiveIntegerField('acima de 60 anos', null=True, blank=True)

    class Meta:
        ordering = ['city', 'pk']
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'

    def __str__(self):
        return self.name

    def max_responses(self):
        if self.n_responses:
            return self.n_responses

        total = 0
        for neighborhood in self.neighborhoods.all():
            total += neighborhood.max_responses or 0
        return total

    def generate_meta(self):
        meta = {
            'total': self.max_responses(),
            'genders': [],
            'age_groups': [],
            'neighborhoods': [],
        }
        meta['genders'] = self.get_gender_surveys()
        meta['age_groups'] = self.get_age_surveys()
        if not self.n_responses:
            neighborhoods = {}
            for neighborhood in self.neighborhoods.all():
                neighborhoods[neighborhood.pk] = {'name': neighborhood.name, 'surveys': neighborhood.max_responses}
            meta['neighborhoods'] = neighborhoods
        return meta

    def get_gender_surveys(self):
        total = self.max_responses()
        values = [round((total*self.city.n_male)/100), round((total*self.city.n_female)/100)]
        while(sum(values) != total):
            if sum(values) > total:
                i = values.index(max(values))
                values[i] -= 1
            else:
                i = values.index(min(values))
                values[i] += 1
        response = {
            '1': {'name': 'Homens', 'value': float(self.city.n_male), 'surveys': self.n_male or values[0]},
            '2':  {'name': 'Mulheres', 'value': float(self.city.n_female), 'surveys': self.n_female or values[1]},
        }
        return response

    def get_age_surveys(self):
        total = self.max_responses()
        values = [
            round((total*self.city.age_group_1)/100),
            round((total*self.city.age_group_2)/100),
            round((total*self.city.age_group_3)/100),
            round((total*self.city.age_group_4)/100),
            round((total*self.city.age_group_5)/100),
        ]
        while(sum(values) != total):
            if sum(values) > total:
                i = values.index(max(values))
                values[i] -= 1
            else:
                i = values.index(min(values))
                values[i] += 1
        response = {
            '1': {'name': '16 a 24 anos', 'value': float(self.city.age_group_1), 'surveys': self.age_group_1 or values[0]},
            '2': {'name': '25 a 34 anos', 'value': float(self.city.age_group_2), 'surveys': self.age_group_2 or values[1]},
            '3': {'name': '35 a 44 anos', 'value': float(self.city.age_group_3), 'surveys': self.age_group_3 or values[2]},
            '4': {'name': '45 a 60 anos', 'value': float(self.city.age_group_4), 'surveys': self.age_group_4 or values[3]},
            '5': {'name': 'Acima de 60 anos', 'value': float(self.city.age_group_5), 'surveys': self.age_group_5 or values[4]},
        }
        return response
        
    max_responses.short_description = "questionários"
    get_gender_surveys.short_description = "divisão por sexo (M|F)"
    get_age_surveys.short_description = "divisão por faixa etária"


class Neighborhood(models.Model):
    name = models.CharField('nome do bairro', max_length=200)
    max_responses = models.PositiveIntegerField('total de questionários', blank=True, null=True)
    sector = models.ForeignKey(Sector, related_name='neighborhoods', verbose_name='setor', on_delete=models.CASCADE)

    class Meta:
        ordering = ['sector', 'name']
        verbose_name = 'Bairro'
        verbose_name_plural = 'Bairros'

    def __str__(self):
        return "{} ({})".format(self.name, self.sector)

    def get_city(self):
        return self.sector.city

    get_city.short_description = "cidade"
