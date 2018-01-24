from django.contrib import admin
from django.utils.html import format_html
from .models import BandImage, Video, Gig


@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):

    def preview_date(self, obj):
        if obj.preview_date_admin:
            return obj.preview_date_admin
        else:
            return obj.preview_date_hidden

    list_display = ['name', 'preview_date']
    fieldsets = [
        ('Gig info', {'fields': ['name', 'gig_link']}),
        ('Date', {'fields': ['gig_date', 'preview_date_admin']}),
        ('Jamboree', {'fields': ['jamboree']}),
    ]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    def thumbnail_image(self, obj):
        if obj.thumbnail:
            return format_html('<img src="%s" style="height: 50px; width: auto">' % (obj.thumbnail.url))
        else:
            "no image"
    thumbnail_image.allow_tags = True
    list_display = ['name', 'thumbnail_image']
    pass

@admin.register(BandImage)
class BandImageAdmin(admin.ModelAdmin):

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="%s" style="height: 50px; width: auto">' % (obj.image.url))
        else:
            "no image"
    thumbnail.allow_tags = True

    list_display = ['thumbnail']
