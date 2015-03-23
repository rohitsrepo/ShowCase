from django.contrib import admin
from compositions.models import Composition
from interpretations.models import Interpretation


class InterpretationInline(admin.StackedInline):
    model = Interpretation
    extra = 2


class CompositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'slug')
    list_filter = ['created']
    search_fields = ['title', 'slug', 'description']
    fields = ['title', 'artist', 'description', 'slug', 'matter']
    inlines = [InterpretationInline]
    

admin.site.register(Composition, CompositionAdmin)