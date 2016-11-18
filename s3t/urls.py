from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('main.urls')),
    url(r'^proveedor/', include('providers.urls', namespace="providers")),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^admin/', admin.site.urls),
]
