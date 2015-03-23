from django.contrib import admin
from feeds.models import StaffPost
from compositions.models import Composition
from interpretations.models import Interpretation


class InterpretationInline(admin.StackedInline):
    model = Interpretation
    extra = 1
    
class CompositionInline(admin.StackedInline):
    model = Composition
    extra = 1
    

class StaffPostAdmin(admin.ModelAdmin):
    list_display = ('composition', 'interpretation')
    fields = ['composition', 'interpretation']

admin.site.register(StaffPost, StaffPostAdmin)