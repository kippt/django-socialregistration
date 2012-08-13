from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from socialregistration.signals import connect

class AppdotnetProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    appdotnet_user = models.CharField(max_length = 255)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.appdotnet_user)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(buffer_user=self.buffer_user)

class AppdotnetAccessToken(models.Model):
    profile = models.OneToOneField(AppdotnetProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)
    
def save_appdotnet_token(sender, user, profile, client, **kwargs):
    try:
        AppdotnetAccessToken.objects.get(profile=profile).delete()
    except AppdotnetAccessToken.DoesNotExist:
        pass
    
    AppdotnetAccessToken.objects.create(access_token = client.get_access_token(),
        profile = profile)


connect.connect(save_appdotnet_token, sender=AppdotnetProfile,
    dispatch_uid='socialregistration_appdotnet_token')
