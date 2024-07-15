from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(DataEntry)
admin.site.register(DataEntry_backup)
admin.site.register(staff_Parameter)

# admin.site.register(Contact)

# from django.contrib import admin

# from .models import City

# class CityAdmin(admin.ModelAdmin):
#     list_display = ("name", "state",)

# admin.site.register(City, CityAdmin)