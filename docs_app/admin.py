from django.contrib import admin
from .models import Document, Query

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'tags')
    search_fields = ('title', 'text', 'tags')
    list_filter = ('date', 'tags')

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('question', 'date')