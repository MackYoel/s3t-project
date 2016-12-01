from django.contrib import admin

from .models import Product, Color, CarSession, Order, OrderItem, Payment

admin.site.register(Product)
admin.site.register(Color)
admin.site.register(CarSession)
admin.site.register(Payment)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    exclude = ('observation',)


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
