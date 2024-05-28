from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from .models import Purchase

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['vm_name', 'vm_cores', 'vm_memory', 'disk_size', 'is_confirmed', 'confirm_button']

    def confirm_button(self, obj):
        if not obj.is_confirmed:
            return format_html('<a class="button" href="{}">Confirm</a>',
                               reverse('admin:admin-confirm-purchase', args=[obj.pk]))
        return 'Confirmed'
    confirm_button.short_description = 'Confirm Purchase'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('confirm/<int:purchase_id>/', self.admin_site.admin_view(self.confirm_purchase), name='admin-confirm-purchase'),
        ]
        return custom_urls + urls

    def confirm_purchase(self, request, purchase_id):
        # Your logic for purchase confirmation
        pass

admin.site.register(Purchase, PurchaseAdmin)
