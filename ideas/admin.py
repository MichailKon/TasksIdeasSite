from django.contrib import admin

from .models import Idea, IdeaType, IdeaTag, IdeaStatus, Difficulty


class TagInline(admin.TabularInline):
    model = Idea.tags.through
    show_change_link = 1
    extra = 1


class IdeaTagAdmin(admin.ModelAdmin):
    inlines = (TagInline, )
    list_display = ('tag', )


admin.site.register(IdeaType)
admin.site.register(IdeaTag, IdeaTagAdmin)
admin.site.register(IdeaStatus)
admin.site.register(Idea)
admin.site.register(Difficulty)
