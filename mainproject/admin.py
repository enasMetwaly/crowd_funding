from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Catogrey, Tag, Image, Project

# Register your models here.
admin.site.register(Catogrey)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Project)

class ProjectAdmin(admin.ModelAdmin):

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        # Add 'is_featured' field to the fieldsets if the user is a superuser
        if request.user.is_superuser:
            fieldsets += (
                ('Additional Options', {'fields': ('is_featured',)}),
            )

        return fieldsets






