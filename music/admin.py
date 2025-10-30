from django.contrib import admin
from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "file", "cover")
    search_fields = ("title", "artist")
