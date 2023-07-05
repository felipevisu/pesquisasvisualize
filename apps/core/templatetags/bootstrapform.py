import django
from django import forms, VERSION as django_version
from django.template import Context
from django.template.loader import get_template
from django import template

register = template.Library()

@register.filter
def bootstrap(element):
    markup_classes = {'label': '', 'value': '', 'single_value': ''}
    return render(element, markup_classes)


@register.filter
def add_input_classes(field):
    field_classes = field.field.widget.attrs.get('class', '')

    if is_date(field):
        field_classes += 'form-control datepicker-input'
        field.field.widget.attrs['data-target'] = '#date_{}'.format(field.id_for_label)
    if is_datetime(field):
        field_classes += 'form-control datetimepicker-input'
        field.field.widget.attrs['data-target'] = '#date_{}'.format(field.id_for_label)
    elif is_select(field):
        field_classes += 'custom-select'
    elif is_checkbox(field) or is_radio(field) or is_multiple_checkbox(field):
        field_classes += 'custom-control-input'
    elif is_file(field):
        field_classes += 'custom-file-input'
    else:
        field_classes += 'form-control'

    if is_textarea(field):
        field.field.widget.attrs['rows'] = 4

    if field.errors:
        field_classes += ' is-invalid'

    field.field.widget.attrs['class'] = field_classes


def render(element, markup_classes):
    element_type = element.__class__.__name__.lower()
    if element_type == 'boundfield':
        add_input_classes(element)
        template = get_template("bootstrapform/field.html")
        context = {'field': element, 'classes': markup_classes, 'form': element.form}
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            for form in element.forms:
                for field in form.visible_fields():
                    add_input_classes(field)

            template = get_template("bootstrapform/formset.html")
            context = {'formset': element, 'classes': markup_classes}
        else:
            for field in element:
                add_input_classes(field)

            template = get_template("bootstrapform/form.html")
            context = {'form': element, 'classes': markup_classes}


    if django_version < (1, 8):
        context = Context(context)

    return template.render(context)


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)

@register.filter
def is_datetime(field):
    return isinstance(field.field.widget, forms.DateTimeInput)

@register.filter
def is_date(field):
    return isinstance(field.field.widget, forms.DateInput)