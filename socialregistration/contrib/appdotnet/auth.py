from django.contrib.sites.models import Site
from socialregistration.contrib.buffer.models import AppdotnetProfile
from django.contrib.auth.backends import ModelBackend


class AppdotnetAuth(ModelBackend):
    def authenticate(self, appdotnet_user = None):
        try:
            return AppdotnetProfile.objects.get(
                appdotnet_user = appdotnet_user,
                site = Site.objects.get_current()).user
        except AppdotnetProfile.DoesNotExist:
            return None
