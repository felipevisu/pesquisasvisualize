from django.contrib import admin

from .models import *

class SectorInline(admin.StackedInline):
    model = Sector
    extra = 0


class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [SectorInline]

    fieldsets = (
        (None, {
           'fields': ['name']
        }),
        ('Divisão por sexo', {
           'fields': ['n_male', 'n_female']
        }),
        ('Divisão por faixa etária', {
            'fields': ['age_group_1', 'age_group_2', 'age_group_3', 'age_group_4', 'age_group_5'],
        }),
    )


class NeighborhoodInline(admin.StackedInline):
    model = Neighborhood
    extra = 0


class SectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']
    list_filter = ['city']
    inlines = [NeighborhoodInline]


class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'sector', 'get_city']
    list_filter = ['sector__city']


admin.site.register(City, CityAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)
