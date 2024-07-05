from django.urls import path

from . import views

app_name = "surveys"
urlpatterns = [
    path("", views.SurveyListView.as_view(), name="list"),
    path(
        "regional/create/",
        views.RegionalSurveyCreateView.as_view(),
        name="regional_create",
    ),
    path(
        "regional/<int:pk>/update/",
        views.RegionalSurveyUpdateView.as_view(),
        name="regional_update",
    ),
    path(
        "regional/<int:pk>/interviewers/",
        views.RegionalSurveyUpdateInterviewersView.as_view(),
        name="regional_interviewers",
    ),
    path(
        "regional/<int:pk>/metas/",
        views.RegionalSurveyMetaView.as_view(),
        name="regional_meta",
    ),
    path(
        "regional/<int:pk>/meta_update/",
        views.MetaUpdateView.as_view(),
        name="meta_update",
    ),
    path(
        "regional/<int:pk>/results/",
        views.RegionalSurveyResultView.as_view(),
        name="regional_results",
    ),
    path("regional/<int:pk>/export/", views.export_survey_xls, name="regional_export"),
    path("open/create/", views.OpenSurveyCreateView.as_view(), name="open_create"),
    path(
        "open/<int:pk>/update/",
        views.OpenSurveyUpdateView.as_view(),
        name="open_update",
    ),
    path(
        "open/<int:pk>/results/",
        views.OpenSurveyResultView.as_view(),
        name="open_results",
    ),
    path("<int:pk>/ordered/", views.SurveyOrderedView.as_view(), name="ordered"),
    path("<int:pk>/delete/", views.SurveyDeleteView.as_view(), name="delete"),
    path(
        "question/<int:pk>/modify/",
        views.QuestionModifyView.as_view(),
        name="question_modify",
    ),
    path(
        "question/<int:pk>/sectors/",
        views.QuestionSectorView.as_view(),
        name="question_sector",
    ),
    path(
        "question/<int:pk>/compare/",
        views.QuestionCompareView.as_view(),
        name="question_compare",
    ),
    path(
        "question/<int:pk>/split/",
        views.QuestionSplitView.as_view(),
        name="question_split",
    ),
]
