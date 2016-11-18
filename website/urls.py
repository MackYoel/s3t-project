from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.panel, name="home"),
    url(r'^providers/$', views.providers, name="providers"),
    url(r'^providers/new/$', views.new_provider, name="new_provider"),
    url(r'^providers/edit/(?P<pk>[0-9]+)/$', views.edit_provider, name="edit_provider"),
    url(r'^products/$', views.products, name="products"),
    url(r'^products/new/$', views.new_product, name="new_product"),
    url(r'^providers/products/edit/(?P<pk>[0-9]+)/$', views.edit_product, name="edit_product"),
    url(r'^car/$', views.car, name="car"),
    url(r'^car-add-product/$', views.car_add_product, name="car_add_product"),
    url(r'^car-remove-product/$', views.car_remove_product, name="car_remove_product"),
    url(r'^car-update-product/$', views.car_update_product, name="car_update_product"),
    url(r'^car-update-order/$', views.car_update_order, name="car_update_order"),
]
