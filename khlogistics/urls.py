
from django.contrib import admin
from django.urls import path, include
from dashboard import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('stock/', include('stock.urls')),
    path('order/', include('order.urls')),
    path('payment/', include('payment.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)