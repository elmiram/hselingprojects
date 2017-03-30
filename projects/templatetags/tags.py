from django import template

register = template.Library()


@register.simple_tag
def lang_link(value, lang):
    prefix = ''
    if value.startswith('/projects'):
        prefix = '/projects'
        value = value[9:]
    value = value[3:] if value.startswith('/en/') else value
    lang = '/en' if lang == 'en' else ''
    return prefix + lang + value
