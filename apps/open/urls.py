from django.urls import path

from apps.responses.views import OpenResponseOpenCreateView, OpenResponseSuccessView

app_name = 'open'
urlpatterns = [
    path('<slug:slug>/', OpenResponseOpenCreateView.as_view(), name="open"),
    path('<slug:slug>/obrigado/', OpenResponseSuccessView.as_view(), name="open_success")
]
