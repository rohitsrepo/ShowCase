from django.contrib import admin
from interpretations.models import Interpretation


class InterpretationAdmin(admin.ModelAdmin):
    list_display = ('composition', 'user', 'interpretation')
    list_filter = ['created']
    search_fields = ['interpretation']
    fields = ['composition', 'user', 'interpretation', 'public']
    
    

admin.site.register(Interpretation, InterpretationAdmin)