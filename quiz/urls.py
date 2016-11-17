from django.conf.urls import url
from quiz.admin_views import *
from quiz.views import *


urlpatterns = [
    # admin views
    url(r'^csv2sql$', csv2sql, name='csv2sql'),

    # regular views
    url(r'^(?P<verb>[,\w]+)/$', verb, name='verb'),
    url(r'^$', main, name='main'),
]

