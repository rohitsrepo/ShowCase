from django.contrib import admin
from compositions.models import Composition
from interpretations.models import Interpretation


class InterpretationInline(admin.StackedInline):
    model = Interpretation
    extra = 2


class CompositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_filter = ['created', 'uploader']
    search_fields = ['title', 'slug', 'description', 'artist__name', 'uploader__name']
    fields = ['title', 'description', 'uploader', 'matter']
    inlines = [InterpretationInline]

    actions = ['add_to_staff_feed']

    def add_to_staff_feed(self, request, queryset):
        for composition in queryset:
        	composition.add_to_staff_feed();
    

admin.site.register(Composition, CompositionAdmin)