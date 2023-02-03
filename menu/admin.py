from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, Dish, DishImage


admin.site.register(Cart)

class DishImageInline(admin.TabularInline):
    model = DishImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')
        return ''


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['title', 'cart', 'description', 'price', 'preparation_time', 'is_vegetarian']
    inlines = [DishImageInline]
    list_filter = ['price', 'last_update']