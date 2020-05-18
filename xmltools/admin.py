from django.contrib import admin

from .models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'file_name', 'profile_file', 'uploaded_at', 'user')

admin.site.register(Document, DocumentAdmin)