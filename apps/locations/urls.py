from django.urls import path

from . import views

app_name = 'locations'
urlpatterns = [
    path('cities/', views.CityListView.as_view(), name='city_list'),
    path('cities/create/', views.CityCreateView.as_view(), name='city_create'),
    path('cities/<int:pk>/update/', views.CityUpdateView.as_view(), name='city_update'),
    path('cities/<int:pk>/delete/', views.CityDeleteView.as_view(), name='city_delete'),
    path('cities/<int:pk>/xls/', views.export_city_xls, name='city_xls'),
    path('sectors/', views.SectorListView.as_view(), name='sector_list'),
    path('sectors/create/', views.SectorCreateView.as_view(), name='sector_create'),
    path('sectors/<int:pk>/update/', views.SectorUpdateView.as_view(), name='sector_update'),
    path('sectors/<int:pk>/delete/', views.SectorDeleteView.as_view(), name='sector_delete'),
    path('neighborhoods/', views.NeighborhoodListView.as_view(), name='neighborhood_list'),
    path('neighborhoods/create/', views.NeighborhoodCreateView.as_view(), name='neighborhood_create'),
    path('neighborhoods/<int:pk>/update/', views.NeighborhoodUpdateView.as_view(), name='neighborhood_update'),
    path('neighborhoods/<int:pk>/delete/', views.NeighborhoodDeleteView.as_view(), name='neighborhood_delete'),
]
