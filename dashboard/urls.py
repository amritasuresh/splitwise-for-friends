from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^dashboard/$', dash),
    url(r'^pdf/$', generate_pdf, name='generate_pdf'),

]