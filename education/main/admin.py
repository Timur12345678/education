from django.contrib import admin
from main.models import SiteUser

class SiteUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(SiteUser, SiteUserAdmin)
# Register your models here.
