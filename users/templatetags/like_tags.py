from django import template
from users.models import Like

register = template.Library()

@register.filter
def has_liked(post, user):
    if post is None or user is None:
        return False
    return Like.objects.filter(post=post, user=user).exists()
