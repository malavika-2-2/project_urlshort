from django.contrib import admin
from .models import Link

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("code", "long_url", "clicks", "created_at")
    search_fields = ("code", "long_url")

