from django.conf.urls import url

from transactions import views
from .views import *


urlpatterns = [
    # all transactions
    url(r'^transactions/$', transactions),
    # only pending transactions
    url(r'^transactions/pending', pending),
    # only completed transactions
    url(r'^transactions/completed', completed),

    # individual transactions
    url(r'^transactions/(?P<transaction_id>[0-9A-Fa-f-]+)/$', views.transaction),

]