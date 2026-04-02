from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'issue_type', 'user', 'status', 'created_at')
    list_filter = ('status', 'issue_type', 'created_at')
    search_fields = ('title', 'description', 'location', 'user__username')
    list_editable = ('status',)
