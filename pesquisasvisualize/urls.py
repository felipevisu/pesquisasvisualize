from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('clients/', include('apps.clients.urls')),
    path('locations/', include('apps.locations.urls')),
    path('responses/', include('apps.responses.urls')),
    path('pesquisas/', include('apps.open.urls')),
    path('', include('apps.surveys.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns

admin.site.site_header = 'Pesquisas Visu'
admin.site.index_title = 'Administração do Sistema'
admin.site.site_title = 'Pesquisas Visu'
