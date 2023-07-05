import django_filters as filters

from apps.responses.models import RegionalResponse, OpenResponse, Answer
from apps.locations.models import Sector, Neighborhood

def question_filter(queryset, name, value):
    answers = Answer.objects.filter(question=int(name), body__contains=value).values('response')
    return queryset.filter(pk__in=answers)

def sample_filter(queryset, name, value):
    size = queryset.count()
    new_size = int(size*value/100)
    return queryset.random(new_size)


class RegionalResponseFilter(filters.FilterSet):

    class Meta:
        model = RegionalResponse
        fields = ['sector', 'neighborhood', 'gender', 'age_group']
    
    def __init__(self, extra, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
 
        self.filters['sample'] = filters.NumberFilter(label="Tamanho da amostra", method=sample_filter)
        self.filters['sector'].queryset = Sector.objects.select_related('city').filter(city=extra['city'])
        self.filters['neighborhood'].queryset = Neighborhood.objects.select_related('sector', 'sector__city').filter(sector__city=extra['city'])
       
        survey = extra['survey']
        for question in survey.questions.all():

            if question.question_type == 'text':
                self.filters[str(question.pk)] = filters.CharFilter(field_name=question.pk, label=question.text, method=question_filter)
            
            if question.question_type in ['radio', 'select', 'select-multiple']:
                self.filters[str(question.pk)] = filters.ChoiceFilter(field_name=question.pk, label=question.text, method=question_filter, choices=question.get_choices())


class OpenResponseFilter(filters.FilterSet):

    class Meta:
        model = OpenResponse
        fields = '__all__'
    
    def __init__(self, extra, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
       
        survey = extra['survey']
        self.filters = {}
        for question in survey.questions.all():

            if question.question_type == 'text':
                self.filters[str(question.pk)] = filters.CharFilter(field_name=question.pk, label=question.text, method=question_filter)
            
            if question.question_type in ['radio', 'select', 'select-multiple']:
                self.filters[str(question.pk)] = filters.ChoiceFilter(field_name=question.pk, label=question.text, method=question_filter, choices=question.get_choices())