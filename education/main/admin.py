from django.contrib import admin
from main.models import SiteUser, CourseCategory, CourseItem, Course, CourseItemParagraph


class SiteUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(SiteUser, SiteUserAdmin)
# Register your models here.

class CourseCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseCategory, CourseCategoryAdmin)


class CourseItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseItem, CourseItemAdmin)


class CourseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Course,  CourseAdmin)


class CourseItemParagraphAdmin(admin.ModelAdmin):
    pass
admin.site.register( CourseItemParagraph,  CourseItemParagraphAdmin)