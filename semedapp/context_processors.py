from .models import Certidao

from .models import Certidao

def pdde_status(request):
    primeiros_tres = Certidao.objects.order_by('id')[:3]
    pdde_habilitado = all(cert.arquivo for cert in primeiros_tres)
    return {'pdde_habilitado': pdde_habilitado}

