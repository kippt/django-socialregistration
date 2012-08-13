from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('appdotnet_button', button('socialregistration/appdotnet/appdotnet_button.html'))