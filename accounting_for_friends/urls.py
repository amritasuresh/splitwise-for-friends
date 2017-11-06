from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from accounting_for_friends import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('accounts.urls')),
    url(r'^', include('dashboard.urls')),
    url(r'^', include('groups.urls')),
    # url(r'^', include('notifications.urls')),
     url(r'^', include('transactions.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
