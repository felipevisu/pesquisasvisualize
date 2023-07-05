from django import template

register = template.Library()

@register.filter(name='fieldtype')
def field_type(field):
    return field.field.widget.__class__.__name__

@register.simple_tag(name='progress')
def progress(actual, meta):
    return int(actual*100/meta)

@register.filter(name='question')
def question(value):
    return 'question' in value