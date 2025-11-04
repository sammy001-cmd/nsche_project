from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AdminProfile
# from .models import AdminProfile, UpgradeOption

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone")
    search_fields = ("user__username", "role")

# @admin.register(UpgradeOption)
# class UpgradeOptionAdmin(admin.ModelAdmin):
#     list_display = ("name", "price", "active")
#     list_filter = ("active",)
#     search_fields = ("name", "description")
