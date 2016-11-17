from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('website.urls')),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^admin/', admin.site.urls),
]
