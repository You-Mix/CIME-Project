from decimal import Decimal
from msilib.schema import tables
from django.contrib import admin

# Register your models here.

from .models import *

from import_export.admin import ImportExportModelAdmin
from import_export import resources

class AdminContrib(admin.ModelAdmin):
    list_display = ('NIU','raison_social','activite','regime_impot','telephone','arrondissement','departement','ug','sous_secteur')

class contribuableRessource(resources.ModelResource):
    class Meta:
        model = contribuable

class contribuableAdmin(ImportExportModelAdmin):
    resource_class = contribuableRessource

admin.site.register(contribuable, AdminContrib)

admin.site.register(UG)
admin.site.register(Sous_secteur)
admin.site.register(Regime_impot)
admin.site.register(Impot)
admin.site.register(Departement)
admin.site.register(Personnel)
admin.site.register(Cellule)
admin.site.register(Service)
admin.site.register(Impot_Declare)
admin.site.register(Declaration)
admin.site.register(Impot_AMR)
admin.site.register(AMR)
admin.site.register(Part_Impot)