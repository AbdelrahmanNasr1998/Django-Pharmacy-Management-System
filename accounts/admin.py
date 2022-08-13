from django.contrib import admin

# Register your models here.
from .models import Accounts, Payments
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea


class UserAdminConfig(UserAdmin):
    model = Accounts
    search_fields = ('email', 'username', 'phone_number')
    list_filter = ('is_active', 'is_staff',)
    ordering = ('-start_date',)
    list_display = ('email', 'username', 'phone_number','billing',
                    'is_active', 'is_block', 'is_staff')
    fieldsets = (
        ('User Information', {'fields': ('username', 'email', 'password', 'phone_number', 'type', 'start_date')}),
        ('User Information', {'fields': ('billing',)}),
        ('Permissions', {'fields': ('is_staff', 'is_block', 'is_active')}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_block', 'is_staff')
        }),
    )



class PaymentsAdmin(admin.ModelAdmin):
    model = Payments
    search_fields = ('username', 'start_billing', 'end_billing', 'ammount')
    list_filter = ('start_billing', 'end_billing')
    ordering = ('end_billing',)
    list_display = ('username', 'start_billing', 'end_billing', 'ammount')
    fieldsets = (
        ('User Payments', {'fields': ('username', 'start_billing', 'end_billing', 'ammount')}),
    )




admin.site.register(Accounts, UserAdminConfig)
admin.site.register(Payments, PaymentsAdmin)