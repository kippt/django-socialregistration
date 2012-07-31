from django.contrib.sites.models import Site
from socialregistration.contrib.buffer.models import BufferProfile
from django.contrib.auth.backends import ModelBackend


class BufferAuth(ModelBackend):
    def authenticate(self, buffer_user = None):
        try:
            return BufferProfile.objects.get(
                buffer_user = buffer_user,
                site = Site.objects.get_current()).user
        except BufferProfile.DoesNotExist:
            return None
