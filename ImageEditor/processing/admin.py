from django.contrib import admin
from core.models import Image


@admin.register(Image)
class SinImgAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_path', 'created_at']
    search_fields = ['img']
    list_filter = ['created_at']

    @admin.display(ordering='img')
    def image_path(self, sinimg):
        return sinimg.img
