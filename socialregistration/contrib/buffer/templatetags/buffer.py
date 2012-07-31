from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('buffer_button', button('socialregistration/buffer/buffer_button.html'))