from django.conf.urls.defaults import *

urlpatterns = patterns("",
    url(r'^futon/(?P<object_id>.*)/$', 'djangocouch.views.futon', name='futon'),
)
