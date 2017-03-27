from django.contrib import admin

from projects.models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'authors')  # в таблице

    def authors(self, instance):
        return ', '.join(a.a_second_name for a in instance.author.all())

admin.site.register(UserProfile)
admin.site.register(DictFile)
admin.site.register(Author)
admin.site.register(Teacher)
admin.site.register(Field)
admin.site.register(Project, ProjectAdmin)
