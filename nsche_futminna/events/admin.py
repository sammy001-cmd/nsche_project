from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import Event, EventRegistration, Resource


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'created_at', 'preview_image')
    list_filter = ('date',)
    search_fields = ('title', 'description')

    # Show image preview in admin list
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit:cover;" />', obj.image.url)
        return "No Image"
    preview_image.short_description = "Image"


class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("student", "event", "registered_at")
    search_fields = ("student__user__username", "event__title")
    list_filter = ("event", "registered_at")
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=registrations.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            writer.writerow(row)

        return response

    export_as_csv.short_description = "Export Selected Registrations to CSV"


# @admin.register(Resource)
# class ResourceAdmin(admin.ModelAdmin):
#     list_display = ('title', 'uploaded_at')
#     search_fields = ('title',)
#     list_filter = ('uploaded_at',)


# ✅ Register models
admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)

# from django.contrib import admin
# from .models import Event, EventRegistration
# from django.http import HttpResponse
# import csv


# class EventAdmin(admin.ModelAdmin):
#     list_display = ('title', 'date', 'location', 'created_at')
#     list_filter = ('date',)
#     search_fields = ('title', 'description')


# class EventRegistrationAdmin(admin.ModelAdmin):
#     list_display = ("student", "event", "registered_at")
#     search_fields = ("student__user__username", "event__title")
#     list_filter = ("event", "registered_at")
#     actions = ["export_as_csv"]

#     def export_as_csv(self, request, queryset):
#         meta = self.model._meta
#         field_names = [field.name for field in meta.fields]

#         response = HttpResponse(content_type="text/csv")
#         response["Content-Disposition"] = "attachment; filename=registrations.csv"
#         writer = csv.writer(response)

#         writer.writerow(field_names)
#         for obj in queryset:
#             row = [getattr(obj, field) for field in field_names]
#             writer.writerow(row)

#         return response

#     export_as_csv.short_description = "Export Selected Registrations to CSV"

# from django.contrib import admin
# from .models import Event, EventRegistration, Resource

# # @admin.register(Resource)
# # class ResourceAdmin(admin.ModelAdmin):
# #     list_display = ('title', 'uploaded_at')
# #     search_fields = ('title',)
# #     list_filter = ('uploaded_at',)



# #  Only register ONCE
# admin.site.register(Event, EventAdmin)
# admin.site.register(EventRegistration, EventRegistrationAdmin)
