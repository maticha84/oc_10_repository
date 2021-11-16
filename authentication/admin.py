from django.contrib import admin
from .models import User
from django.db import models


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
