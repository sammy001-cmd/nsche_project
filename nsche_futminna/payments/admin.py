from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Payment
import csv
from django.http import HttpResponse

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status', 'reference', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('student__user__username', 'reference')
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        field_names = [field.name for field in Payment._meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=payments.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            writer.writerow(row)

        return response

    export_as_csv.short_description = "Export Selected Payments to CSV"

admin.site.register(Payment, PaymentAdmin)
