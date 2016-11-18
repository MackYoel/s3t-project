from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.panel, name="home"),
    url(r'^products/$', views.product_list, name="product_list"),
    url(r'^products/new/$', views.product_new, name="product_new"),
    url(r'^products/edit/(?P<pk>[0-9]+)/$', views.product_edit, name="product_edit"),
    url(r'^orders/list/$', views.order_list, name="order_list"),
    url(r'^orders/edit/(?P<pk>[0-9]+)/$', views.order_edit, name="order_edit"),
]
