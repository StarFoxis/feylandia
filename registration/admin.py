from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'skill_all')
    list_display_links = ('name',)
    ordering = ('id',)

class SkinAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image')
    readonly_fields = ('get_image',)
    ordering = ('name',)
    exclude = ('cost',)
    save_as = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')
    get_image.short_description = 'Изображение'

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'required_level', 'required_mana')
    feildsets = (
        (None, {
            'fields': ('name', 'desc')
        }),
        ('Требования', {
            'fields': ('required_level', 'required_mana')
        }),
    )

class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'style', 'active')
    readonly_fields = ('user', 'active', 'level',)
    fieldsets = (
        ('Персонаж', {
            'fields': ('user', 'style', 'skin', 'active')
        }),
        ('Расходники', {
            'fields': (('health', 'mana', 'coins'),)
        }),
        ('Уровень', {
            'classes': ('collapse',),
            'fields': ('level',)
        }),
    )


    class Meta:
        model = PersonModel
        ordering = 'user__username'


admin.site.register(PersonModel, PersonAdmin)
admin.site.register(StyleModel, StyleAdmin)
admin.site.register(SkillModel, SkillAdmin)
admin.site.register(SkinModel, SkinAdmin)

admin.site.site_title = 'Фейляндия'
admin.site.site_header = 'Фейляндия'