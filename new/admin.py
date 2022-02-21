from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'created')


@admin.register(Order)
class ElonAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'name', 'category','discount', 'created', 'active', 'price')
