from django.contrib import admin
from .models import *

# Register your models here.

class SurgeryAdmin(admin.ModelAdmin):
    list_display = ['subject', 'location', 'date_time']

class WeighingAdmin(admin.ModelAdmin):
    list_display = ['subject', 'weight']

class NoteAdmin(admin.ModelAdmin):
    list_display = ['subject', 'narrative']

admin.site.register(Note, NoteAdmin)
admin.site.register(Weighing, WeighingAdmin)
admin.site.register(Surgery, SurgeryAdmin)
admin.site.register(Experiment)
admin.site.register(OtherAction)
admin.site.register(ProcedureType)
admin.site.register(WaterAdministration)

admin.site.register(VirusInjection)
