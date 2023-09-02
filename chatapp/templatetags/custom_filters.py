from django import template

register = template.Library()

@register.filter
def is_f_request_sent(id,f_request):
    return any(id== f.receiver.id for f in f_request)