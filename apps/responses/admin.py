from django.contrib import admin

from .models import *


class AnswerInline(admin.StackedInline):
    model = Answer
    fields = ["question", "body"]
    readonly_fields = [
        "question",
    ]
    extra = 0


class OpenResponseAdmin(admin.ModelAdmin):
    list_display = ["pk", "creation_date"]
    inlines = [AnswerInline]


class RegionalResponseAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "city",
        "sector",
        "neighborhood",
        "gender",
        "age_group",
        "creation_date",
    ]
    inlines = [AnswerInline]

    def get_queryset(self, request):
        return (
            RegionalResponse.objects.all()
            .select_related("city", "sector", "neighborhood")
            .prefetch_related("answers")
        )


admin.site.register(Response)
admin.site.register(OpenResponse, OpenResponseAdmin)
admin.site.register(RegionalResponse, RegionalResponseAdmin)
