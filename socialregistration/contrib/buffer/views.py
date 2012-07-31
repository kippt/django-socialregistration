from django.core.urlresolvers import reverse
from socialregistration.contrib.buffer.client import Buffer
from socialregistration.contrib.buffer.models import BufferProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class BufferRedirect(OAuthRedirect):
    client = Buffer
    template_name = 'socialregistration/buffer/buffer.html'

class BufferCallback(OAuthCallback):
    client = Buffer
    template_name = 'socialregistration/buffer/buffer.html'
    
    def get_redirect(self):
        return reverse('socialregistration:buffer:setup')

class BufferSetup(SetupCallback):
    client = Buffer
    profile = BufferProfile
    template_name = 'socialregistration/buffer/buffer.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'buffer_user': client.get_user_info()['_id']}
    
