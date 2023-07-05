import xlwt
from django.http import HttpResponse

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from extra_views import (CreateWithInlinesView, InlineFormSetFactory,
                         UpdateWithInlinesView)

from apps.core.mixins import SuccessURLMixin

from .models import City, Neighborhood, Sector


class CityListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = City
    paginate_by = 10
    permission_required = ['locations.view_city']

    def get_queryset(self):
        return City.objects.annotate(
            n_sectors=Count('sectors', distinct=True), n_neighborhoods=Count('sectors__neighborhoods')
            ).order_by('name')


class SectorInline(InlineFormSetFactory):
    model = Sector
    fields = ['name', 'n_responses']
    factory_kwargs = {'extra': 0}


class CityCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessURLMixin, CreateWithInlinesView):
    model = City
    inlines = [SectorInline]
    fields = '__all__'
    permission_required = ['locations.add_city']
    success_url = 'locations:city_update'
    success_url_new = 'locations:city_create'
    success_url_close = 'locations:city_list'


class CityUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessURLMixin, UpdateWithInlinesView):
    model = City
    inlines = [SectorInline]
    fields = '__all__'
    permission_required = ['locations.change_city']
    success_url = 'locations:city_update'
    success_url_new = 'locations:city_create'
    success_url_close = 'locations:city_list'


class CityDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = City
    permission_required = ['locations.delete_city']
    success_url = reverse_lazy('locations:city_list')


class SectorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Sector
    paginate_by = 10
    permission_required = ['locations.view_sector']

    def get_queryset(self):
        return Sector.objects.annotate(n_neighborhoods=Count('neighborhoods')).order_by('city', 'pk')


class NeighborhoodInline(InlineFormSetFactory):
    model = Neighborhood
    fields = ['name', 'max_responses']
    factory_kwargs = {'extra': 0}


class SectorCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessURLMixin, CreateWithInlinesView):
    model = Sector
    inlines = [NeighborhoodInline]
    fields = '__all__'
    permission_required = ['locations.add_sector']
    success_url = 'locations:sector_update'
    success_url_new = 'locations:sector_create'
    success_url_close = 'locations:sector_list'


class SectorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessURLMixin, UpdateWithInlinesView):
    model = Sector
    inlines = [NeighborhoodInline]
    fields = '__all__'
    permission_required = ['locations.change_sector']
    success_url = 'locations:sector_update'
    success_url_new = 'locations:sector_create'
    success_url_close = 'locations:sector_list'


class SectorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Sector
    permission_required = ['locations.delete_sector']
    success_url = reverse_lazy('locations:sector_list')


class NeighborhoodListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Neighborhood
    paginate_by = 20
    permission_required = ['locations.view_neighborhood']


class NeighborhoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessURLMixin, CreateView):
    model = Neighborhood
    fields = ['name', 'sector', 'max_responses']
    permission_required = ['locations.add_neighborhood']
    success_url = 'locations:neighborhood_update'
    success_url_new = 'locations:neighborhood_create'
    success_url_close = 'locations:neighborhood_list'


class NeighborhoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessURLMixin, UpdateView):
    model = Neighborhood
    fields = ['name', 'sector', 'max_responses']
    permission_required = ['locations.change_neighborhood']
    success_url = 'locations:neighborhood_update'
    success_url_new = 'locations:neighborhood_create'
    success_url_close = 'locations:neighborhood_list'


class NeighborhoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Neighborhood
    permission_required = ['locations.delete_neighborhood']
    success_url = reverse_lazy('locations:neighborhood_list')


def export_city_xls(request, pk):
    city = City.objects.get(pk=pk)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(city.name)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(city.name)
    font_style = xlwt.XFStyle()

    index = 0

    col = ["", "", "Homem", "Mulher", "16 a 24 anos", "25 a 34 anos", "35 a 44 anos", "45 a 59 anos", "60 anos"]
    for row in range(len(col)):
        ws.write(row, index, col[row], font_style)

    index += 1

    col = ["", ""]
    for gender in city.get_gender_surveys().values():
        col.append('{}%'.format(gender['value']))
    for age in city.get_age_surveys().values():
        col.append('{}%'.format(age['value']))
    for row in range(len(col)):
        ws.write(row, index, col[row], font_style)

    index += 1

    for i, sector in enumerate(city.sectors.all()):
        col = []
        col.append("Setor {}".format(i+1))
        col.append(sector.max_responses())
        for gender in sector.get_gender_surveys().values():
            col.append(gender['surveys'])
        for age in sector.get_age_surveys().values():
            col.append(age['surveys'])
        for row in range(len(col)):
            ws.write(row, index, col[row], font_style)
        index += 1

    col = []
    col.append("Total")
    col.append(city.max_responses())
    for gender in city.get_gender_surveys().values():
        col.append(gender['surveys'])
    for age in city.get_age_surveys().values():
        col.append(age['surveys'])
    for row in range(len(col)):
        ws.write(row, index, col[row], font_style)

    wb.save(response)
    return response