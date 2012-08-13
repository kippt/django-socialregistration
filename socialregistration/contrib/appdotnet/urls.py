from django.conf import settings
from django.conf.urls.defaults import *
from socialregistration.contrib.appdotnet.views import AppdotnetRedirect, \
    AppdotnetCallback, AppdotnetSetup
 
urlpatterns = patterns('',
    url('^redirect/$', AppdotnetRedirect.as_view(), name='redirect'),
    url('^callback/$', AppdotnetCallback.as_view(), name='callback'),
    url('^setup/$', AppdotnetSetup.as_view(), name='setup'),
)
