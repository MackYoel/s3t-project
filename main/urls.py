from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.panel, name="home"),
    url(r'^providers/$', views.provider_list, name="provider_list"),
    url(r'^providers/new/$', views.provider_new, name="provider_new"),
    url(r'^providers/edit/(?P<pk>[0-9]+)/$', views.provider_edit, name="provider_edit"),
    url(r'^car/$', views.car, name="car"),
    url(r'^car-add-product/$', views.car_add_product, name="car_add_product"),
    url(r'^car-remove-product/$', views.car_remove_product, name="car_remove_product"),
    url(r'^car-update-product/$', views.car_update_product, name="car_update_product"),
    url(r'^car-update-order/$', views.car_update_order, name="car_update_order"),
    url(r'^car-create-orders/$', views.car_create_orders, name="car_create_orders"),
    url(r'^orders-list/$', views.order_list, name="order_list"),
    url(r'^orders-edit/(?P<pk>[0-9]+)/$', views.order_edit, name="order_edit"),
]
