from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth2
from socialregistration.settings import SESSION_KEY
import json
import urllib
import httplib2

class Appdotnet(OAuth2):
    client_id = getattr(settings, 'APPDOTNET_CLIENT_ID', '')
    secret = getattr(settings, 'APPDOTNET_CLIENT_SECRET', '')
    scope = getattr(settings, 'APPDOTNET_REQUEST_PERMISSIONS', '')
    
    auth_url = 'https://alpha.app.net/oauth/authenticate'
    access_token_url = 'https://alpha.app.net/oauth/access_token'
    
    _user_info = None
    
    def client(self):
        return httplib2.Http(disable_ssl_certificate_validation=True)
    
    def get_callback_url(self):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('socialregistration:appdotnet:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('socialregistration:appdotnet:callback'))

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
        return super(Appdotnet, self).get_access_token(grant_type='authorization_code', **params)

    def get_user_info(self):
        if self._user_info is None:
            resp, content = self.client().request('https://alpha-api.app.net/stream/0/users/me?%s' % urllib.urlencode({'access_token':self._access_token}), method="GET")
            self._user_info = json.loads(content)['data']
        return self._user_info
    
    @staticmethod
    def get_session_key():
        return '%sappdotnet' % SESSION_KEY
