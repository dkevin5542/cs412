from django.contrib import admin
from .models import *
from .models import AudioFile, Video


# Register your models here.
admin.site.register(Profile)
admin.site.register(Anime)
admin.site.register(Character)
admin.site.register(Merchandise)


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'anime', 'uploaded_at')
    list_filter = ('anime', 'uploaded_at')
    search_fields = ('title', 'anime__title')


