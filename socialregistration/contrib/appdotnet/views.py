from django.core.urlresolvers import reverse
from socialregistration.contrib.appdotnet.client import Appdotnet
from socialregistration.contrib.appdotnet.models import AppdotnetProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class AppdotnetRedirect(OAuthRedirect):
    client = Appdotnet
    template_name = 'socialregistration/appdotnet/appdotnet.html'

class AppdotnetCallback(OAuthCallback):
    client = Appdotnet
    template_name = 'socialregistration/appdotnet/appdotnet.html'
    
    def get_redirect(self):
        return reverse('socialregistration:appdotnet:setup')

class AppdotnetSetup(SetupCallback):
    client = Appdotnet
    profile = AppdotnetProfile
    template_name = 'socialregistration/appdotnet/appdotnet.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'appdotnet_user': client.get_user_info()['id']}

