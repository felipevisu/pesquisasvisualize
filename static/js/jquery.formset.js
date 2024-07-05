function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(prefix) {
    var selector = '.' + prefix + '-empty';
    var selector_name = prefix + '-empty';
    var newElement = $(selector).clone(true);
    newElement.removeClass('d-none');
    newElement.removeClass(selector_name);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function () {
        var name = $(this).attr('name').replace('-' + '__prefix__' + '-', '-' + total + '-');
        var id = $(this).attr('id').replace('-' + '__prefix__' + '-', '-' + total + '-');
        $(this).attr({
            'name': name,
            'id': id
        })
    });
    newElement.find('label').each(function () {
        var forValue = $(this).attr('for');
        if (forValue) {
            forValue = forValue.replace('-' + '__prefix__' + '-', '-' + total + '-');
            $(this).attr({
                'for': forValue
            });
        }
    });
    total++;
    newElement.find(":input[name*='order']").first().val(total);
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    var putIn = '.' + prefix + '-list';
    $(putIn).append(newElement);
    return false;
}

function deleteForm(prefix, btn) {
    var elemName = '.' + prefix + '-list .' + prefix + '-row';
    btn.closest(elemName).remove();
    var forms = $(elemName);
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    for (var i = 0, formCount = forms.length; i < formCount; i++) {
        $(forms.get(i)).find(':input').each(function () {
            updateElementIndex(this, prefix, i);
        });
        $(forms.get(i)).find(":input[name*='order']").first().val(i+1);
    }
    return false;
}

$(document).on('click', '.add-row', function (e) {
    e.preventDefault();
    var prefix = $(this).data('prefix');
    console.log(prefix)
    cloneMore(prefix);
    return false;
});

$(document).on('click', '.delete-row', function (e) {
    e.preventDefault();
    var prefix = $(this).data('prefix');
    deleteForm(prefix, $(this));
    return false;
});