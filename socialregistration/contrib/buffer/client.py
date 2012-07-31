from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth2
from socialregistration.settings import SESSION_KEY
import json
import urllib


class Buffer(OAuth2):
    client_id = getattr(settings, 'BUFFER_CLIENT_ID', '')
    secret = getattr(settings, 'BUFFER_ACCESS_TOKEN', '')
    scope = getattr(settings, 'BUFFER_REQUEST_PERMISSIONS', '')
    
    auth_url = 'https://bufferapp.com/oauth2/authorize'
    access_token_url = 'https://api.bufferapp.com/1/oauth2/token.json'
    
    _user_info = None
    
    def get_callback_url(self):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('socialregistration:buffer:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('socialregistration:buffer:callback'))

    def request_access_token(self, params):
        """ 
        Buffer requires correct content-type for POST requests
        """
        return self.client().request(self.access_token_url, method="POST", body=urllib.urlencode(params), headers={'Content-Type':'application/x-www-form-urlencoded'})
    
    def parse_access_token(self, content):
        """
        Parse access_token from returning JSON
        """
        return json.loads(content)
    
    def get_access_token(self, **params):
        """
        Buffer requires grant_type
        """
        return super(Buffer, self).get_access_token(grant_type='authorization_code', **params)

    def get_user_info(self):
        if self._user_info is None:
            resp, content = self.client().request('https://api.bufferapp.com/1/user.json?%s' % urllib.urlencode({'access_token':self._access_token}), method="GET")
            self._user_info = json.loads(content)
        return self._user_info
    
    @staticmethod
    def get_session_key():
        return '%sbuffer' % SESSION_KEY
