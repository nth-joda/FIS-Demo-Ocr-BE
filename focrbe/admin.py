from django.contrib import admin
from .models import Detection
# Register your models here.


class DetectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'type', 'result', 'created', 'updated')
    list_filter = ('id', 'type', 'result', 'created', 'updated')
    search_fields = ('type', 'result', 'created', 'updated')
    date_hierarchy = 'created'
    ordering = ('-created',)
    readonly_fields = ['created', 'updated']
    fieldsets = (
        (None, {
            'fields': ('image', 'type', 'result')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created', 'updated')
        }),
    )


admin.site.register(Detection, DetectionAdmin)
