from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from models import *
from error_reporting.models import ErrorReport
from utils.admin import GenericAdmin


class ThematicAreaLocalAdmin(admin.TabularInline):
    model = ThematicAreaLocal
    extra = 0


class ThematicAreaAdmin(GenericAdmin):
    model = ThematicArea
    inlines = [ThematicAreaLocalAdmin, ]


class SourceTypeLocalAdmin(admin.TabularInline):
    model = SourceTypeLocal
    extra = 0


class SourceTypeAdmin(GenericAdmin):
    model = SourceType
    inlines = [SourceTypeLocalAdmin, ]


class DescriptorAdmin(generic.GenericTabularInline):
    model = Descriptor
    extra = 1


class KeywordAdmin(generic.GenericTabularInline):
    model = Keyword
    extra = 1


class ResourceThematicAdmin(admin.TabularInline):
    model = ResourceThematic
    extra = 1


class ErrorReportAdmin(generic.GenericTabularInline):
    model = ErrorReport
    extra = 1


class ResourceAdmin(GenericAdmin):
    model = Resource
    date_hierarchy = 'created_time'
    list_display = ('id', 'title', 'link', 'created_by', 'status')
    search_fields = ['id', 'title']
    list_filter = ('status', 'source_language__language', 'source_type__name', 'thematics__thematic_area', 'cooperative_center_code')
    inlines = [DescriptorAdmin, KeywordAdmin, ErrorReportAdmin, ]

admin.site.register(Resource, ResourceAdmin)
admin.site.register(ThematicArea, ThematicAreaAdmin)
