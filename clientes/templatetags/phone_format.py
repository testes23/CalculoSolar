from django import template
from django.utils.html import format_html


register = template.Library()

@register.filter
def format_phone(phone):
    """
    Formata o número de telefone.
    Se tiver 11 dígitos, formata como (XX) XXXXX-XXXX.
    Se tiver 10 dígitos, formata como (XX) XXXX-XXXX.
    """
    phone_str = str(phone)
    if len(phone_str) == 11:
        return f"({phone_str[:2]}) {phone_str[2:7]}-{phone_str[7:]}"
    elif len(phone_str) == 10:
        return f"({phone_str[:2]}) {phone_str[2:6]}-{phone_str[6:]}"
    return phone_str

@register.filter
def format_doc(doc):
    doc_str= ''.join(filter(str.isdigit,doc))
    if len(doc_str) == 11:
        return format_html('{}.{}.{}-{}',doc_str[:3],doc_str[3:6],doc_str[6:9],doc_str[9:])
    elif len(doc_str):
        return format_html('{}.{}.{}/{}-{}',doc_str[:2],doc_str[2:5],doc_str[5:8],doc_str[8:12],doc_str[12:])
    return doc_str

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def format_type(doc):
    if doc == 'PF':
        return 'Pessoa Fisica'
    else:
        return 'Pessoa Jurídica'