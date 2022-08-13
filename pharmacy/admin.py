from django.contrib import admin

# Register your models here.
from .models import Category, Medicine, Payment, Items, Settings
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    search_fields = ('name', 'username')
    list_filter = ('name', 'username')
    ordering = ('name', 'username')
    list_display = ('name', 'username')
    fieldsets = (
        ('Category Information', {'fields': ('name', 'username')}),
    )


class MedicineAdmin(admin.ModelAdmin):
    model = Category
    search_fields = ('name', 'category', 'username')
    list_filter = ('name', 'category')
    ordering = ('name', 'category', 'price', 'quantity')
    list_display = ('name', 'category', 'username', 'price', 'quantity')
    fieldsets = (
        ('Name & Category Information', {'fields': ('name', 'category', 'username')}),
        ('Price & Quantity Information', {'fields': ('price', 'quantity')}),
        ('Notes Information', {'fields': ('notes',)}),
        ('Start & End Date Information', {'fields': ('start_date', 'end_date')}),
    )


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    search_fields = ('username', 'date', 'total')
    list_filter = ('username', 'date', 'total')
    ordering = ('username', 'date', 'total')
    list_display = ('username', 'date', 'total')
    fieldsets = (
        ('Payment Information', {'fields': ('username', 'data', 'date', 'total')}),
    )

class SettingsAdmin(admin.ModelAdmin):
    model = Settings
    search_fields = ('username', 'days', 'qty')
    list_filter = ('username', 'days', 'qty')
    ordering = ('username', 'days', 'qty')
    list_display = ('username', 'days', 'qty')
    fieldsets = (
        ('Payment Information', {'fields': ('username', 'days', 'qty')}),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Items)
