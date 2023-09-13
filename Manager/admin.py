from django.contrib import admin

from Manager.models import CustomUser,Teacher
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Teacher)