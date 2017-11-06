from django.conf.urls import url
from .views import *


urlpatterns = [
    # all transactions
    url(r'^transactions/$', transactions),
]