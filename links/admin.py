from django.contrib import admin

# Register your models here.
from .models import link
from django.contrib.auth.admin import UserAdmin
from .models import collection


admin.site.register(link)
admin.site.register(collection)

#admin.site.register(User, UserAdmin)
