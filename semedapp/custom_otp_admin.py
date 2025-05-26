from django.contrib import admin
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice

# Remove os registros automáticos antes de registrar novamente
if admin.site.is_registered(TOTPDevice):
    admin.site.unregister(TOTPDevice)

if admin.site.is_registered(StaticDevice):
    admin.site.unregister(StaticDevice)

# Registros personalizados
@admin.register(TOTPDevice)
class SafeTOTPAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'confirmed', 'last_t')
    search_fields = ('user__username', 'user__email')
    list_filter = ('confirmed',)

    def last_t(self, obj):
        return getattr(obj, 'last_t', '-')


@admin.register(StaticDevice)
class SafeStaticDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'confirmed')
    search_fields = ('user__username', 'user__email')
    list_filter = ('confirmed',)
