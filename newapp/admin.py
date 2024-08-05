from django.contrib import admin
from .models import Customer, Product, Order
from django.utils.translation import gettext_lazy as _


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('email', 'phone_number')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'total_bill', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'customer', 'product')
    search_fields = ('customer__first_name', 'customer__last_name', 'product__name')

    def save_model(self, request, obj, form, change):
    
        obj.total_bill = obj.quantity * obj.product.price
        super().save_model(request, obj, form, change)


class PriceRangeFilter(admin.SimpleListFilter):
    title = _('price range')
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return [
            ('0-50', _('Up to $50')),
            ('51-100', _('From $51 to $100')),
            ('101-500', _('From $101 to $500')),
            ('501-1000', _('From $501 to $1000')),
            ('1001-5000', _('Above $1000')),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            min_price, max_price = map(int, value.split('-'))
            return queryset.filter(price__gte=min_price, price__lte=max_price)
        return queryset
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    list_filter = (PriceRangeFilter,)  


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)