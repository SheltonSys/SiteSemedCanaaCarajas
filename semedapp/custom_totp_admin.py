from django.contrib import admin
from django_otp.plugins.otp_totp.models import TOTPDevice

@admin.register(TOTPDevice)
class CustomTOTPDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'confirmed', 'user', 'last_t:otp')
    search_fields = ('user__username', 'user__email')
    list_filter = ('confirmed',)
