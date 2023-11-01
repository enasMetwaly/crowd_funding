from django.contrib import admin


from .models import *

admin.site.register(Catogrey)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Project)

class ProjectAdmin(admin.ModelAdmin):

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            fieldsets += (
                ('Additional Options', {'fields': ('is_featured',)}),
            )
        return fieldsets






