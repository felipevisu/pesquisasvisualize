from django.urls import path

from . import views

app_name = 'responses'
urlpatterns = [
    path('open/<int:pk>/create/', views.OpenResponseCreateView.as_view(), name='open_create'),
    path('regional/<int:pk>/create/', views.RegionalResponseCreateView.as_view(), name='regional_create'),
]
