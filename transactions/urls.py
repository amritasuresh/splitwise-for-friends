from django.conf.urls import url

from transactions import views
from .views import *


urlpatterns = [
    # all transactions
    url(r'^transactions/$', transactions),
    # only pending transactions
    url(r'^transactions/pending/$', pending),
    # only completed transactions
    url(r'^transactions/completed/$', completed),

    # individual transactions
    url(r'^transactions/(?P<transaction_id>[0-9A-Fa-f-]+)/$', views.transaction),

    # transaction operations
    url(r'^transactions/(?P<transaction_id>[0-9A-Fa-f-]+)/pay/$', views.pay),
    url(r'^transactions/(?P<transaction_id>[0-9A-Fa-f-]+)/delete/$', views.delete),

    # transaction resolution
    url(r'^transactions/resolution/$', resolution),
    url(r'^transactions/resolution/(?P<user_id>[0-9]+)/$', resolve_balance)

]