from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('accounts.urls')),
    url(r'^', include('groups.urls')),
    # url(r'^', include('notifications.urls')),
    # url(r'^', include('transactions.urls')),
]
