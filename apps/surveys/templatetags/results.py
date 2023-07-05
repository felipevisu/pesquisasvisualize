import json

from django import template
from django.db.models import Count
from django.template.loader import render_to_string
from django.db.models import Q

register = template.Library()

from apps.responses.models import Response, Answer
from apps.surveys.models import Question


@register.simple_tag
def results_list(question, responses, answers):
    responses = responses.values('id')
    responses = list(responses)
    responses_ids = [res['id'] for res in responses]
    answers = [answer for answer in answers if answer['question'] == question.id and answer['response'] in responses_ids]

    options = []
    for answer in answers:
        if answer['body'] not in options:
            options.append(answer['body'])

    results = []
    for option in sorted(options):
        total = len([answer for answer in answers if answer['body'] == option])
        results.append({
            'option': option,
            'total': total
        })

    return render_to_string('charts/results_list.html', {'results': results, 'total': len(responses) })


@register.simple_tag
def simple_pie_chart(question, responses, answers):
    responses_ids = responses.values_list('id', flat=True)
    answers = [answer for answer in answers if answer['question']==question.id and answer['response'] in responses_ids]
    series = []
    options = question.get_choices_list()

    for option in options:
        item = {
            'name': option,
            'y': len([answer for answer in answers if option in answer['body']]),
        }
        series.append(item)

    chart = {'series': series}
    return render_to_string('charts/pie.html', {'chart': chart, 'question': question })


@register.simple_tag
def sectors_pie_chart(responses, sectors):
    responses = responses.values('id', 'sector')
    responses = list(responses)

    series = []

    for sector in sectors:
        item = {
            'name': sector['name'],
            'y': len([response for response in responses if response['sector'] == sector['id']])
        }
        series.append(item)

    chart = {'series': series}
    return render_to_string('charts/sectors_pie.html', {'chart': chart })


@register.simple_tag
def agr_group_pie_chart(responses):
    responses = responses.values('id', 'age_group')
    responses = list(responses)

    series = []

    ages = [
        (1, '16 a 24'),
        (2, '25 a 34'),
        (3, '35 a 44'),
        (4, '45 a 60'),
        (5, 'Acima de 60')
    ]

    for age in ages:
        item = {
            'name': age[1],
            'y': len([response for response in responses if response['age_group'] == age[0]])
        }
        series.append(item)

    chart = {'series': series}
    return render_to_string('charts/age_group_pie.html', {'chart': chart })


@register.simple_tag
def gender_pie_chart(responses):
    responses = responses.values('id', 'gender')
    responses = list(responses)

    series = []

    genders = [
        (1, 'Masculino'),
        (2, 'Feminino')
    ]

    for gender in genders:
        item = {
            'name': gender[1],
            'y': len([response for response in responses if response['gender'] == gender[0]])
        }
        series.append(item)

    chart = {'series': series}
    return render_to_string('charts/gender_pie.html', {'chart': chart })


@register.simple_tag
def pie_chart(question, responses, sectors, answers):
    responses = responses.values('id', 'sector')
    responses = list(responses)
    responses_ids = [res['id'] for res in responses]

    answers = [answer for answer in answers if answer['question']==question.id and answer['response'] in responses_ids]
    series = []
    options = question.get_choices_list()

    for option in options:
        item = {
            'name': option,
            'y': len([answer for answer in answers if option in answer['body']]),
            'drilldown': option
        }
        series.append(item)

    drilldown = []

    for option in options:

        item = {}
        item['name'] = option
        item['id'] = option
        item['data'] = []
        for index, sector in enumerate(sectors):
            resps = [res['id'] for res in responses if res['sector'] == sector['id']]
            total = len([answer for answer in answers if option in answer['body'] and answer['response'] in resps])
            if total > 0:
                item['data'].append(["Setor {}".format(index+1), total])
        drilldown.append(item)

    chart = {'series': series, 'drilldown': drilldown}
    return render_to_string('charts/pie_drilldown.html', {'chart': chart, 'question': question })


@register.simple_tag
def simple_column_chart(question, responses, answers):
    responses_ids = responses.values_list('id', flat=True)
    answers = [answer for answer in answers if answer['question']==question.id and answer['response'] in responses_ids]
    series = []
    options = question.get_choices_list()

    for option in options:
        item = {
            'name': option,
            'y': len([answer for answer in answers if option in answer['body']]),
        }
        series.append(item)

    chart = {'series': series,}
    return render_to_string('charts/column.html', {'chart': chart, 'question': question })


@register.simple_tag
def column_chart(question, responses, sectors, answers):
    responses = responses.values('id', 'sector')
    responses = list(responses)
    responses_ids = [res['id'] for res in responses]

    answers = [answer for answer in answers if answer['question']==question.id and answer['response'] in responses_ids]
    series = []
    options = question.get_choices_list()

    for option in options:
        item = {
            'name': option,
            'y': len([answer for answer in answers if option in answer['body']]),
            'drilldown': option
        }
        series.append(item)

    drilldown = []

    for option in options:

        item = {}
        item['name'] = option
        item['id'] = option
        item['data'] = []
        for index, sector in enumerate(sectors):
            resps = [res['id'] for res in responses if res['sector'] == sector['id']]
            total = len([answer for answer in answers if option in answer['body'] and answer['response'] in resps])
            if total > 0:
                item['data'].append(["Reg {}".format(index+1), total])
        drilldown.append(item)

    chart = {'series': series, 'drilldown': drilldown}
    return render_to_string('charts/column_drilldown.html', {'chart': chart, 'question': question })
    

@register.simple_tag
def sector_chart(question, responses, sectors, answers):
    responses = responses.values('id', 'sector')
    responses = list(responses)
    responses_ids = [res['id'] for res in responses]

    answers = [answer for answer in answers if answer['question']==question.id and answer['response'] in responses_ids]

    categories = []
    for index, sector in enumerate(sectors):
        categories.append("Reg {}".format(index+1))
    
    series = []
    options = question.get_choices_list()

    for option in options:
        item = {}
        item['name'] = option
        item['data'] = []
        for index, sector in enumerate(sectors):
            resps = [res['id'] for res in responses if res['sector'] == sector['id']]
            resps_total = len(resps)
            if resps_total == 0:
                item['data'].append(0)
            else:
                total = len([answer for answer in answers if option in answer['body'] and answer['response'] in resps])
                x = round((total*100)/resps_total, 2)
                item['data'].append(x)
        series.append(item)
        
    chart = {'series': series, 'categories': categories}
    return render_to_string('charts/sector.html', {'chart': chart, 'question': question })


@register.simple_tag
def compare_chart(question, sector):
    questions = Question.objects.filter(key=question.key, survey__city=question.survey.city).order_by('pk')
    options = question.get_choices_list()

    categories = []
    for question in questions:
        categories.append(question.survey.creation_date.strftime('%b'))
    
    series = []
    for option in options:
        item = {}
        data = []
        for question in questions:
            if sector:
                answers = Answer.objects.filter(question=question, response__regionalresponse__sector=sector)
            else:
                answers = Answer.objects.filter(question=question)

            total = answers.count()

            if total > 0:
                resps = answers.filter(body__contains=option).count()
                x = round((resps*100)/total, 2)
                data.append(x)
            else:
                data.append(0)

        item['name'] = option
        item['data'] = data
        series.append(item)

    chart = {'series': series, 'categories': categories}
    return render_to_string('charts/compare.html', {'chart': chart, 'question': question })