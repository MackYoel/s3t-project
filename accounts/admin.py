from django.contrib import admin
from . models import Person
# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'ruc', 'account_number', 'bank')


admin.site.register(Person, PersonAdmin)
