from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from semedapp import views  # Substitua "semedapp" pelo nome do seu app

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),  # Rota raiz aponta para index
    # path("semedapp/", include("semedapp.urls")),  # Inclua outras rotas
    path('', include('semedapp.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('conselho/', include('semedapp.urls')),
    path('conselho/planetario/', include('semedapp.urls')),  # Substitua `semedapp` pelo nome do seu app
    path('banco-curriculos/', include('semedapp.urls')),  # Inclua as rotas do app sem namespace
    #path('banco_curriculos/', include('banco_curriculos.urls')),  # Inclua as URLs do app
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)