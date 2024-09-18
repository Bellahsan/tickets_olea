# myapp/templatetags/custom_tags.py

from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_user_avatar(user):
    if user.profile_image:
        return user.profile_image.url
    return settings.STATIC_URL + 'images/profile_image.jpg'
