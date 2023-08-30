from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Database, Empleados, Event

class DatabaseResource(resources.ModelResource):
    class Meta:
        model = Database
        #model = Empleados

class EmpleadosResource(resources.ModelResource):
    class Meta: 
        model = Empleados

class EventResource(resources.ModelResource):
    class Meta:
        model = Event

admin.site.register(Event)

class userdat(ImportExportModelAdmin):
    resource_class = DatabaseResource

class empldat(ImportExportModelAdmin):
    resource_class = EmpleadosResource

admin.site.register(Database, userdat) #
admin.site.register(Empleados, empldat)

