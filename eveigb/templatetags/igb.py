from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('eveigb/open_mail.html', takes_context=True)
def eve_mail_link(context):
    """ Provide a link either to in-game mail, or EVE Gate mail"""
    return {
        'igb': context['is_igb'],
        'gate_base': getattr(settings, 'EVE_GATE_BASE', 'https://gate.eveonline.com')
    }
