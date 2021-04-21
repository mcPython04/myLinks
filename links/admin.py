from django.contrib import admin

# Register your models here.
from .models import link
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.register(link)

#admin.site.register(User, UserAdmin)
