from django.contrib import admin

from .models import Question, RegionalSurvey, OpenSurvey, RegionalSurveyInterviewer

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    

class RegionalSurveyInterviewerInline(admin.StackedInline):
    model = RegionalSurveyInterviewer
    extra = 0

class RegionalSurveyAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'client', 'creation_date']
    inlines = [QuestionInline, RegionalSurveyInterviewerInline]


class OpenSurveyAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'creation_date']
    inlines = [QuestionInline]


admin.site.register(RegionalSurvey, RegionalSurveyAdmin)
admin.site.register(OpenSurvey, OpenSurveyAdmin)
