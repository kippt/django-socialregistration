from django.conf import settings
from django.conf.urls.defaults import *
from socialregistration.contrib.buffer.views import BufferRedirect, \
    BufferCallback, BufferSetup
 
urlpatterns = patterns('',
    url('^redirect/$', BufferRedirect.as_view(), name='redirect'),
    url('^callback/$', BufferCallback.as_view(), name='callback'),
    url('^setup/$', BufferSetup.as_view(), name='setup'),
)
