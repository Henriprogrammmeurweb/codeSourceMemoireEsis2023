from django.contrib import admin
from django.conf.urls import handler403, handler404,handler500
from django.urls import path,include
from django.conf.urls.static import static
from .import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("AppAccount.urls")),
    path('personnel/', include('AppPersonnel.urls')),
    path('conge/', include('AppConge.urls')),
    path('planning/', include('AppPlanning.urls'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = "AppAccount.views.page403"
handler404 = "AppAccount.views.page404"
handler500 = "AppAccount.views.page500"



