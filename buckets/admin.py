from django.contrib import admin

from .models import Bucket

from compositions.models import Composition

class CompositionInline(admin.StackedInline):
    model = Bucket.compositions.through

class BucketAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'views', 'compositions_count', 'created')
    list_filter = ['created', 'owner']
    search_fields = ['name', 'owner__name']
    fields = ['name', 'description', 'background']
    inlines = [CompositionInline]

    actions = ['add_to_staff_feed']

    def add_to_staff_feed(self, request, queryset):
        for bucket in queryset:
        	bucket.add_to_staff_feed();

admin.site.register(Bucket, BucketAdmin)
