from django.contrib import admin

from .models import *

# admin.site.register(CatalogHasDBOperation)
# admin.site.register(CatalogHasRequestOperation)
#admin.site.register(CatalogHasVariables)

# admin.site.register(ChunkHasDBOperation)
# admin.site.register(ChunkHasRequestOperation)
admin.site.register(DBOperation)
admin.site.register(OperationLog)
admin.site.register(Report)
admin.site.register(Parameter)
admin.site.register(Header)
admin.site.register(Extractor)
admin.site.register(Function)


class VaribaleInline(admin.StackedInline):
    model = Variable
    extra = 1


class RequestInline(admin.StackedInline):
    model = RequestOperation
    extra = 1


class DBInline(admin.StackedInline):
    model = DBOperation
    extra = 1


class CatalogAdmin(admin.ModelAdmin):
    fields = ['parent', 'name', 'desc', 'status', 'priority', 'type']
    inlines = [VaribaleInline,RequestInline,DBInline]

admin.site.register(Catalog, CatalogAdmin)
