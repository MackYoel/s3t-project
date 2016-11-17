from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.panel, name="home"),
    url(r'^providers/$', views.providers, name="providers"),
    url(r'^providers/new/$', views.new_provider, name="new_provider"),
    url(r'^providers/edit/(?P<pk>[0-9]+)/$', views.edit_provider, name="edit_provider"),
    url(r'^providers/setpassword/(?P<token>.*)/$', views.set_password_provider, name="set_password_provider"),
    url(r'^products/$', views.products, name="products"),
    url(r'^providers/products/new/$', views.new_product, name="new_product"),
]
