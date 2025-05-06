
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.shortcuts import render
import qrcode
from io import BytesIO
import base64

@login_required
def gerar_qr(request):
    user = request.user
    device, created = TOTPDevice.objects.get_or_create(user=user, name="SIEDGE 2FA")

    if created or not device.confirmed:
        uri = device.config_url
        qr = qrcode.make(uri)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        qr_b64 = base64.b64encode(buffer.getvalue()).decode()
        return render(request, 'siedge_2fa/ativar_2fa.html', {"qr_code": qr_b64})
    else:
        return render(request, 'siedge_2fa/ativar_2fa.html', {"msg": "2FA já está ativo para sua conta."})
