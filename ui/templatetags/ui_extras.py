from django import template
register = template.Library()

@register.simple_tag
def get_cases(module_id):
    #return Catalog.objects.all().filter(type='Case', parent__id=module_id)
    return  'fffff'