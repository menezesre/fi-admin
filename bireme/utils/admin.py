from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from models import *


class GenericAdmin(admin.ModelAdmin):
    exclude = ()

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'updater') and hasattr(obj, 'creator'):
            if change:
                obj.updated_by = request.user
            else:
                obj.created_by = request.user
                obj.updated_by = request.user
        obj.save()


class CountryLocalAdmin(admin.TabularInline):
    model = CountryLocal
    extra = 0

class CountryAdmin(GenericAdmin):
    model = Country
    inlines = [CountryLocalAdmin,]
    search_fields = list_display = ['code', 'name']

class ContentTypeAdmin(GenericAdmin):
    model = ContentType
    list_display = ['pk', 'name']
    search_fields = ['name',]


admin.site.register(Country, CountryAdmin)

admin.site.register(ContentType, ContentTypeAdmin)