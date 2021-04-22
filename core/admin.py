from django.contrib import admin
from .models import Product, Transaction, Calorie
from .forms import TransactionCreationForm, TransactionChangeForm

admin.site.register(Product)
admin.site.register(Calorie)


class TransactionAdmin(admin.ModelAdmin):
    change_form = TransactionChangeForm
    add_form = TransactionCreationForm

    date_hierarchy = 'date'
    raw_id_fields = ['product', 'bought_by']
    list_filter = ['date', ]

    def add_view(self, request, form_url='', extra_context=None):
        self.fieldsets = (
            (None, {'fields': ('product', 'quantity', 'bought_by')}),
        )
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fieldsets = (
            (None, {'fields': ('product', 'quantity', 'total_amount', 'bought_by',)}),
        )
        return super().change_view(request, object_id, form_url, extra_context)

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form
        return super().get_form(request, obj, change, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.bought_by.save()
        obj.save()

    list_display = ['id', 'date', 'amount']
    ordering = ('-date',)


admin.site.register(Transaction, TransactionAdmin)
