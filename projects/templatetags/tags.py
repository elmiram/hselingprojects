from django import template

register = template.Library()


@register.simple_tag
def lang_link(value, lang):
    value = value[3:] if value.startswith('/en/') else value
    lang = '/en' if lang == 'en' else ''
    prefix = ''
    if value.startswith('/projects'):
        prefix = '/projects'
        value = value[9:]
    return prefix + lang + value
